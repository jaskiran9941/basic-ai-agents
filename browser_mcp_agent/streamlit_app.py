"""
Browser MCP Agent - Streamlit UI
Control your web browser using natural language commands through a web interface
"""

import streamlit as st
import subprocess
import os
import asyncio
import threading
from pathlib import Path
from openai import OpenAI
from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor

# Page configuration
st.set_page_config(
    page_title="Browser MCP Agent",
    page_icon="🌐",
    layout="wide"
)


class BrowserController:
    """Manages browser instance with dedicated event loop thread"""

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.is_running = False
        self.loop = None
        self.thread = None
        self.executor = ThreadPoolExecutor(max_workers=1)

    def _run_event_loop(self, loop):
        """Run event loop in dedicated thread"""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def _ensure_loop(self):
        """Ensure we have a running event loop"""
        if self.loop is None or not self.loop.is_running():
            self.loop = asyncio.new_event_loop()
            self.thread = threading.Thread(target=self._run_event_loop, args=(self.loop,), daemon=True)
            self.thread.start()

    def _run_async(self, coro):
        """Run coroutine in the dedicated event loop"""
        self._ensure_loop()
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result(timeout=30)

    async def _async_start_browser(self, url: str):
        """Async browser launch"""
        if not self.is_running:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            self.is_running = True

        if url:
            await self.page.goto(url)

    def start_browser(self, url: str = "https://google.com"):
        """Launch browser and navigate to URL"""
        try:
            self._run_async(self._async_start_browser(url))
            return "Browser launched and ready!"
        except Exception as e:
            return f"❌ Failed to start browser: {str(e)}"

    async def _async_execute_goal(self, goal: str, api_key: str, progress_callback=None) -> str:
        """Execute a high-level goal autonomously with multiple steps"""
        if not self.is_running:
            return "❌ Browser not started. Please enter a URL first!"

        try:
            # Validate API key
            if not api_key or not api_key.strip():
                return "❌ API key is missing. Please enter it in the sidebar."

            client = OpenAI(api_key=api_key.strip())

            if progress_callback:
                progress_callback("🤖 Agent started. Analyzing goal...")

            # Get current page state
            page_content = await self.page.text_content("body")
            page_url = self.page.url
            page_title = await self.page.title()

            # Agent conversation history
            conversation = []
            max_steps = 15  # Prevent infinite loops
            step_count = 0

            while step_count < max_steps:
                step_count += 1

                if progress_callback:
                    progress_callback(f"🔄 Step {step_count}: Planning next action...")

                # Build the agent prompt
                system_prompt = """You are an autonomous web browser agent. You can:
1. Navigate to URLs
2. Click elements (provide CSS selector)
3. Fill forms (provide CSS selector and value)
4. Scroll pages (up/down with pixel amounts)
5. Get page content

Analyze the goal and current page state. Decide the NEXT SINGLE action to take.
If the goal is complete, respond with {"status": "complete", "summary": "what was accomplished"}
Otherwise, respond with ONE action in this format:
{"action": "navigate|click|fill|scroll|get_content", "selector": "css_selector_if_needed", "value": "value_if_needed", "url": "url_if_navigate", "reasoning": "why this action"}"""

                # Create the planning message
                planning_message = f"""GOAL: {goal}

CURRENT STATE:
- URL: {page_url}
- Page Title: {page_title}
- Page Content (first 2000 chars): {page_content[:2000]}

STEPS TAKEN SO FAR: {step_count - 1}
{chr(10).join([f"- {msg['content']}" for msg in conversation[-3:]])}

What is the NEXT action to achieve the goal? Respond with JSON only."""

                conversation.append({"role": "user", "content": planning_message})

                # Ask GPT to plan next action
                response = client.chat.completions.create(
                    model="gpt-4",
                    max_tokens=1024,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *conversation
                    ]
                )

                # Parse response
                import json
                response_text = response.choices[0].message.content.strip()

                # Remove markdown code blocks if present
                if response_text.startswith('```'):
                    lines = response_text.split('\n')
                    response_text = '\n'.join(lines[1:-1])

                decision = json.loads(response_text)
                conversation.append({"role": "assistant", "content": response_text})

                # Check if goal is complete
                if decision.get("status") == "complete":
                    if progress_callback:
                        progress_callback(f"✅ Goal complete: {decision.get('summary', 'Task finished')}")
                    return f"✅ **Goal Complete!**\n\n{decision.get('summary', 'Task finished successfully')}\n\n**Steps taken:** {step_count}"

                # Execute the action
                action_desc = decision.get('reasoning', 'Executing action')
                if progress_callback:
                    progress_callback(f"⚙️ {action_desc}")

                result = await self._async_execute_action(decision)

                if progress_callback:
                    progress_callback(f"✓ {result}")

                # Update page state for next iteration
                await asyncio.sleep(1)  # Brief pause for page to update
                page_content = await self.page.text_content("body")
                page_url = self.page.url
                page_title = await self.page.title()

                # Add result to conversation
                conversation.append({"role": "user", "content": f"Action result: {result}"})

            return f"⚠️ **Goal partially complete** - Reached maximum {max_steps} steps.\n\nThe agent may need more steps or the goal might need to be simplified."

        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def _async_execute_command(self, command: str, api_key: str) -> str:
        """Execute a single browser command (legacy support)"""
        if not self.is_running:
            return "❌ Browser not started. Please enter a URL first!"

        try:
            # Validate API key
            if not api_key or not api_key.strip():
                return "❌ API key is missing. Please enter it in the sidebar."

            client = OpenAI(api_key=api_key.strip())

            # Ask GPT to convert natural language to specific browser actions
            response = client.chat.completions.create(
                model="gpt-4",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""Given this browser command: "{command}"

Convert it to ONE specific browser action. Respond with ONLY a JSON object in this format:
{{"action": "navigate|click|fill|scroll|get_content", "selector": "css_selector_if_needed", "value": "value_if_needed", "url": "url_if_navigate"}}

Examples:
- "go to github.com" → {{"action": "navigate", "url": "https://github.com"}}
- "click the search button" → {{"action": "click", "selector": "button[aria-label='Search']"}}
- "scroll down" → {{"action": "scroll", "value": "500"}}
- "scroll up" → {{"action": "scroll", "value": "-500"}}
- "scroll down 1000px" → {{"action": "scroll", "value": "1000"}}
- "fill the search box with hello" → {{"action": "fill", "selector": "input[type='search']", "value": "hello"}}

For scroll actions: use positive numbers for scrolling down, negative for scrolling up. Default to 500 for down, -500 for up.

Respond with ONLY the JSON, nothing else."""
                }]
            )

            # Extract the JSON response
            import json
            action_text = response.choices[0].message.content

            # Parse the action
            action_text = action_text.strip()
            # Remove markdown code blocks if present
            if action_text.startswith('```'):
                lines = action_text.split('\n')
                action_text = '\n'.join(lines[1:-1])

            action = json.loads(action_text)

            # Execute the action (async)
            result = await self._async_execute_action(action)
            return result

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def execute_goal(self, goal: str, api_key: str, progress_callback=None) -> str:
        """Execute autonomous goal using dedicated event loop"""
        try:
            # Wrapper for progress callback to work with threading
            def thread_safe_callback(msg):
                if progress_callback:
                    progress_callback(msg)

            async def run_with_callback():
                return await self._async_execute_goal(goal, api_key, thread_safe_callback)

            return self._run_async(run_with_callback())
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def execute_command(self, command: str, api_key: str, mode: str = "auto") -> str:
        """Execute command or goal based on mode

        mode: 'command' (single action), 'goal' (autonomous), 'auto' (detect)
        """
        try:
            if mode == "auto":
                # Detect if this is a multi-step goal vs single command
                goal_indicators = [
                    "and then", "after that", "find", "search for", "get the",
                    "compare", "collect", "list", "save", "download"
                ]
                is_goal = any(indicator in command.lower() for indicator in goal_indicators)

                if is_goal or len(command.split()) > 10:
                    mode = "goal"
                else:
                    mode = "command"

            if mode == "goal":
                return self.execute_goal(command, api_key)
            else:
                return self._run_async(self._async_execute_command(command, api_key))
        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def _async_execute_action(self, action: dict) -> str:
        """Execute the browser action (async)"""
        try:
            action_type = action.get("action")

            if action_type == "navigate":
                url = action.get("url", "")
                if not url.startswith("http"):
                    url = "https://" + url
                await self.page.goto(url)
                return f"✅ Navigated to {url}"

            elif action_type == "click":
                selector = action.get("selector", "")
                await self.page.click(selector, timeout=5000)
                return f"✅ Clicked element: {selector}"

            elif action_type == "fill":
                selector = action.get("selector", "")
                value = action.get("value", "")
                await self.page.fill(selector, value)
                return f"✅ Filled '{selector}' with '{value}'"

            elif action_type == "scroll":
                value = action.get("value", "500")
                # Handle direction keywords or numeric values
                if isinstance(value, str):
                    if value.lower() == "down":
                        amount = 500
                    elif value.lower() == "up":
                        amount = -500
                    else:
                        try:
                            amount = int(value)
                        except ValueError:
                            amount = 500
                else:
                    amount = int(value)

                await self.page.evaluate(f"window.scrollBy(0, {amount})")
                direction = "down" if amount > 0 else "up"
                return f"✅ Scrolled {direction} {abs(amount)}px"

            elif action_type == "get_content":
                content = await self.page.text_content("body")
                return f"📄 Page content:\n{content[:500]}..."

            else:
                return f"❌ Unknown action: {action_type}"

        except Exception as e:
            return f"❌ Action failed: {str(e)}\nTry being more specific or use different selectors."

    async def _async_close(self):
        """Close browser (async)"""
        if self.is_running:
            try:
                if self.page:
                    await self.page.close()
            except:
                pass
            try:
                if self.browser:
                    await self.browser.close()
            except:
                pass
            try:
                if self.playwright:
                    await self.playwright.stop()
            except:
                pass
            self.is_running = False

    def close(self):
        """Close browser and cleanup"""
        try:
            if self.is_running:
                self._run_async(self._async_close())
        except:
            pass
        finally:
            # Stop the event loop
            if self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(self.loop.stop)
            self.loop = None
            self.thread = None


# Initialize browser controller in session state
if 'browser' not in st.session_state:
    st.session_state.browser = BrowserController()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Title and header
st.title("🌐 Browser MCP Agent")
st.markdown("Control your web browser using natural language commands")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Initialize API key from environment if not in session
    if 'api_key' not in st.session_state:
        env_key = os.environ.get("OPENAI_API_KEY", "")
        st.session_state.api_key = env_key
        if env_key:
            st.success(f"✅ API key loaded ({env_key[:10]}...)")

    # API Key input
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your OpenAI API key (or loaded from .env)",
        key="api_key_input"
    )

    # Update session state if changed
    if api_key_input and api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        os.environ["ANTHROPIC_API_KEY"] = api_key_input

    # Use the session state value - CRITICAL: make sure we actually have it
    api_key = st.session_state.api_key if st.session_state.api_key else api_key_input

    # Debug: show if key is actually loaded
    if api_key:
        st.caption(f"🔑 Using key: {api_key[:15]}...")
    else:
        st.warning("⚠️ No API key detected")

    st.divider()

    # URL Input and Launch
    st.header("🚀 Launch Browser")
    url_input = st.text_input(
        "Enter URL to open",
        value="https://github.com",
        placeholder="https://example.com"
    )

    if st.button("🌐 Open Browser", type="primary"):
        if not api_key:
            st.error("⚠️ Please enter your API key first")
        else:
            with st.spinner("Launching browser..."):
                result = st.session_state.browser.start_browser(url_input)
                st.success(result)
                st.session_state.messages.append({
                    "role": "system",
                    "content": f"🚀 Browser opened at {url_input}"
                })

    # Browser status
    status_color = "🟢" if st.session_state.browser.is_running else "🔴"
    status_text = "Running" if st.session_state.browser.is_running else "Not Started"
    st.markdown(f"{status_color} **Browser:** {status_text}")

    st.divider()

    # Agent Mode Selection
    st.header("🤖 Agent Mode")
    agent_mode = st.radio(
        "Select mode:",
        options=["auto", "command", "goal"],
        index=0,
        help="Auto: detects if input is command or goal\nCommand: single action\nGoal: autonomous multi-step"
    )

    if 'agent_mode' not in st.session_state:
        st.session_state.agent_mode = "auto"
    st.session_state.agent_mode = agent_mode

    if agent_mode == "command":
        st.info("💬 **Command Mode**: Each input = one action")
    elif agent_mode == "goal":
        st.info("🎯 **Goal Mode**: Agent works autonomously until goal complete")
    else:
        st.info("🔮 **Auto Mode**: Automatically detects command vs goal")

    st.divider()

    # Example commands
    st.header("💡 Examples")

    with st.expander("🔹 Simple Commands (1 action)"):
        st.markdown("""
        - go to reddit.com
        - click the search button
        - scroll down
        - fill the search box with "claude"
        """)

    with st.expander("🎯 Complex Goals (multi-step)"):
        st.markdown("""
        - Go to GitHub and search for "playwright python"
        - Find the most popular Python web frameworks and list them
        - Navigate to news.ycombinator.com and get the top 3 story titles
        - Go to Reddit, search for "AI agents", and click the first result
        """)


    st.divider()

    # Close browser button
    if st.button("🗑️ Close Browser"):
        st.session_state.browser.close()
        st.session_state.messages = []
        st.rerun()

# Main content area - Chat interface
mode = st.session_state.get('agent_mode', 'auto')
if mode == "goal":
    st.header("🎯 Autonomous Agent Interface")
    st.caption("Give the agent a high-level goal and watch it work autonomously")
elif mode == "command":
    st.header("💬 Command Interface")
    st.caption("Execute single browser actions")
else:
    st.header("🔮 Smart Interface")
    st.caption("Automatically detects if you want a command or autonomous goal")

# Display chat history
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] in ["assistant", "system"] else msg["role"]
    with st.chat_message(role):
        st.markdown(msg["content"])

# Command input with dynamic placeholder
placeholder_text = {
    "command": "Enter a single command (e.g., 'scroll down')...",
    "goal": "Enter a goal (e.g., 'Find the top 3 Python repos on GitHub')...",
    "auto": "Enter a command or goal..."
}

if prompt := st.chat_input(placeholder_text.get(mode, "Enter a command..."), key="command_input"):
    # Get API key and mode from session state
    current_api_key = st.session_state.get('api_key', '')
    current_mode = st.session_state.get('agent_mode', 'auto')

    if not current_api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar")
    elif not st.session_state.browser.is_running:
        st.error("⚠️ Please launch the browser first using the sidebar")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Execute with progress tracking
        with st.chat_message("assistant"):
            # Create a placeholder for progress updates
            progress_placeholder = st.empty()
            result_placeholder = st.empty()

            progress_messages = []

            def update_progress(msg):
                progress_messages.append(msg)
                progress_placeholder.markdown("\n\n".join(progress_messages))

            # Execute based on mode
            if current_mode == "goal":
                update_progress("🤖 **Agent Mode: Autonomous Goal Execution**")
                result = st.session_state.browser.execute_goal(prompt, current_api_key, update_progress)
            else:
                # Auto or command mode
                result = st.session_state.browser.execute_command(prompt, current_api_key, current_mode)

            # Clear progress and show final result
            progress_placeholder.empty()
            result_placeholder.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})

# Footer
st.divider()

mode_help = {
    "command": "Each input executes ONE action in the browser. You control every step.",
    "goal": "Give a high-level goal. The agent plans and executes multiple steps autonomously.",
    "auto": "Smart mode: Simple inputs = single command. Complex inputs = autonomous goal."
}

st.markdown(f"""
<div style='text-align: center; color: gray; padding: 10px;'>
    <strong>Current Mode: {mode.upper()}</strong><br>
    {mode_help.get(mode, "")}
</div>
""", unsafe_allow_html=True)
