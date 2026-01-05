"""
Test script for the Content Discovery Agent.

This demonstrates various use cases and shows how the agent adapts
its behavior based on different types of topics.
"""

from agent import ContentDiscoveryAgent
import sys
import os

# Add parent directory to path so we can import agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_technical_topic():
    """Test with a technical topic - should use web, GitHub, and books."""
    print("\n" + "=" * 70)
    print("TEST 1: Technical Topic (AI Product Management)")
    print("=" * 70)
    print("\nExpected behavior:")
    print("- Should search web for articles and blogs")
    print("- Should search GitHub for relevant repos/tools")
    print("- Should search books for comprehensive guides")
    print()

    agent = ContentDiscoveryAgent()
    result = agent.discover("AI Product Management", verbose=True)

    print("\n📊 Analysis:")
    print(f"Tools used: {[t['tool'] for t in result['tools_used']]}")
    print(f"Cost: ${result['estimated_cost']:.4f}")


def test_parenting_topic():
    """Test with a parenting topic - should NOT use GitHub."""
    print("\n" + "=" * 70)
    print("TEST 2: Parenting Topic (Making Kids Listen)")
    print("=" * 70)
    print("\nExpected behavior:")
    print("- Should search web for parenting advice")
    print("- Should search books for parenting guides")
    print("- Should NOT search GitHub (not a technical topic)")
    print()

    agent = ContentDiscoveryAgent()
    result = agent.discover("making kids listen", verbose=True)

    print("\n📊 Analysis:")
    print(f"Tools used: {[t['tool'] for t in result['tools_used']]}")
    print(f"Cost: ${result['estimated_cost']:.4f}")

    # Check if agent correctly avoided GitHub
    tools = [t['tool'] for t in result['tools_used']]
    if 'github_search' in tools:
        print("⚠️  WARNING: Agent used GitHub for non-technical topic")
    else:
        print("✅ GOOD: Agent correctly avoided GitHub for parenting topic")


def test_relationship_topic():
    """Test with a relationship topic."""
    print("\n" + "=" * 70)
    print("TEST 3: Relationship Topic (Being a Better Partner)")
    print("=" * 70)
    print("\nExpected behavior:")
    print("- Should search web for relationship advice")
    print("- Should search books for psychology/relationship books")
    print("- Should NOT search GitHub")
    print()

    agent = ContentDiscoveryAgent()
    result = agent.discover("being a better partner after 9 years of marriage", verbose=True)

    print("\n📊 Analysis:")
    print(f"Tools used: {[t['tool'] for t in result['tools_used']]}")
    print(f"Cost: ${result['estimated_cost']:.4f}")


def test_custom_topic():
    """Test with a user-provided topic."""
    print("\n" + "=" * 70)
    print("TEST 4: Custom Topic")
    print("=" * 70)

    topic = input("\nEnter your topic: ").strip()
    if not topic:
        print("No topic provided. Skipping.")
        return

    agent = ContentDiscoveryAgent()
    result = agent.discover(topic, verbose=True)

    print("\n📊 Analysis:")
    print(f"Tools used: {[t['tool'] for t in result['tools_used']]}")
    print(f"Cost: ${result['estimated_cost']:.4f}")


def run_all_tests():
    """Run all test cases."""
    print("\n🧪 Running Content Discovery Agent Tests")
    print("=" * 70)

    try:
        test_technical_topic()
        input("\nPress Enter to continue to next test...")

        test_parenting_topic()
        input("\nPress Enter to continue to next test...")

        test_relationship_topic()
        input("\nPress Enter for custom topic test...")

        test_custom_topic()

        print("\n" + "=" * 70)
        print("✅ All tests completed!")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")


if __name__ == "__main__":
    run_all_tests()
