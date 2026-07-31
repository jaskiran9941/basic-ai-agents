import { useEffect, useMemo, useState } from 'react'
import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  BadgeCheck,
  BarChart3,
  Bell,
  Box,
  CalendarDays,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  CircleDollarSign,
  Clock3,
  Eye,
  FileCheck2,
  Flag,
  Globe2,
  Headphones,
  Heart,
  HelpCircle,
  Info,
  Languages,
  LockKeyhole,
  MapPin,
  MessageCircle,
  PackageCheck,
  Plane,
  Play,
  Radio,
  ReceiptText,
  RotateCcw,
  Search,
  Settings2,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  Store,
  TrendingUp,
  Truck,
  Users,
  WandSparkles,
  X,
  Zap,
} from 'lucide-react'
import './App.css'
import {
  buyerStages,
  catalogueItems,
  destinationOptions,
  euCountries,
  experienceTenets,
  marketGroups,
  productImages,
  sellerStages,
} from './data'

const cx = (...classes) => classes.filter(Boolean).join(' ')

function initialStageFor(role, max) {
  const params = new URLSearchParams(window.location.search)
  if (params.get('role') !== role) return 0
  const stage = Number(params.get('stage'))
  return Number.isInteger(stage) ? Math.min(Math.max(stage, 0), max) : 0
}

function EbayLogo() {
  return (
    <div className="ebay-logo" aria-label="eBay">
      <span className="logo-e">e</span>
      <span className="logo-b">b</span>
      <span className="logo-a">a</span>
      <span className="logo-y">y</span>
    </div>
  )
}

function Button({
  children,
  variant = 'primary',
  icon: Icon,
  iconPosition = 'right',
  className,
  ...props
}) {
  return (
    <button className={cx('button', `button-${variant}`, className)} {...props}>
      {Icon && iconPosition === 'left' && <Icon size={17} strokeWidth={2} />}
      <span>{children}</span>
      {Icon && iconPosition === 'right' && <Icon size={17} strokeWidth={2} />}
    </button>
  )
}

function Badge({ children, tone = 'neutral', icon: Icon }) {
  return (
    <span className={cx('badge', `badge-${tone}`)}>
      {Icon && <Icon size={13} />}
      {children}
    </span>
  )
}

function SectionHeading({ eyebrow, title, description, action }) {
  return (
    <div className="section-heading">
      <div>
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        <h2>{title}</h2>
        {description && <p className="section-description">{description}</p>}
      </div>
      {action}
    </div>
  )
}

function Avatar({ label = 'AT', small = false }) {
  return <span className={cx('avatar', small && 'avatar-small')}>{label}</span>
}

function formatLocalPrice(euros, destination, includeCode = false) {
  const rate = destination.code === 'PL' ? 4.28 : destination.code === 'SE' ? 11.15 : 1
  const value = Math.round(euros * rate)
  if (destination.currency === '€') {
    return `${includeCode ? 'EUR ' : '€'}${value.toLocaleString('en-US')}`
  }
  return `${value.toLocaleString('en-US')} ${destination.currency}`
}

function StageNav({ role, stages, activeIndex, onSelect }) {
  return (
    <div className="stage-nav-wrap">
      <div className="stage-nav" aria-label={`${role} journey`}>
        {stages.map((stage, index) => (
          <button
            key={stage.id}
            className={cx(
              'stage-step',
              index === activeIndex && 'stage-step-active',
              index < activeIndex && 'stage-step-complete',
            )}
            onClick={() => onSelect(index)}
          >
            <span className="stage-number">
              {index < activeIndex ? <Check size={13} strokeWidth={3} /> : stage.short}
            </span>
            <span className="stage-copy">
              <strong>{stage.label}</strong>
              <small>{stage.helper}</small>
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}

function AppHeader({ role, onRoleChange, destination, onDestinationChange, onOpenBlueprint }) {
  const [destinationOpen, setDestinationOpen] = useState(false)

  return (
    <header className="app-header">
      <div className="brand-lockup">
        <EbayLogo />
        <span className="brand-divider" />
        <span className="live-mark">
          <Radio size={15} fill="currentColor" />
          LIVE
        </span>
        <span className="eu-chip">EU concept</span>
      </div>

      <div className="role-switch" aria-label="Choose journey">
        <button
          className={cx(role === 'seller' && 'active')}
          onClick={() => onRoleChange('seller')}
        >
          <Store size={16} />
          Seller
        </button>
        <button
          className={cx(role === 'buyer' && 'active')}
          onClick={() => onRoleChange('buyer')}
        >
          <ShoppingBag size={16} />
          Buyer
        </button>
      </div>

      <div className="header-actions">
        {role === 'buyer' && (
          <div className="destination-picker">
            <button
              className="destination-trigger"
              onClick={() => setDestinationOpen((open) => !open)}
              aria-expanded={destinationOpen}
            >
              <span>{destination.flag}</span>
              <span className="destination-copy">
                <small>Delivering to</small>
                <strong>{destination.city}</strong>
              </span>
              <ChevronDown size={15} />
            </button>
            {destinationOpen && (
              <div className="destination-menu">
                <p>Choose your destination</p>
                {destinationOptions.map((option) => (
                  <button
                    key={option.code}
                    className={cx(option.code === destination.code && 'selected')}
                    onClick={() => {
                      onDestinationChange(option)
                      setDestinationOpen(false)
                    }}
                  >
                    <span>{option.flag}</span>
                    <span>
                      <strong>{option.city}</strong>
                      <small>{option.name}</small>
                    </span>
                    {option.code === destination.code && <Check size={15} />}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
        <button className="blueprint-trigger" onClick={onOpenBlueprint}>
          <Sparkles size={16} />
          <span>Experience logic</span>
        </button>
        <button className="icon-button" aria-label="Help">
          <HelpCircle size={19} />
        </button>
        <button className="icon-button notification-button" aria-label="Notifications">
          <Bell size={19} />
          <span />
        </button>
        <Avatar label={role === 'seller' ? 'AT' : 'CM'} small />
      </div>
    </header>
  )
}

function PageIntro({ step, total, label, title, description, children }) {
  return (
    <div className="page-intro">
      <div>
        <div className="page-kicker">
          <span>
            {String(step).padStart(2, '0')} / {String(total).padStart(2, '0')}
          </span>
          <span>{label}</span>
        </div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {children}
    </div>
  )
}

function RegistrationScreen({ onContinue, notify }) {
  const [confirmed, setConfirmed] = useState({ origin: true, identity: true, returns: false })
  const readyCount = marketGroups.ready.length

  const toggle = (key) => {
    setConfirmed((current) => ({ ...current, [key]: !current[key] }))
  }

  return (
    <>
      <PageIntro
        step={1}
        total={5}
        label="Spring registration"
        title="One setup. A much bigger room."
        description="Turn your next live show into a trusted EU-wide event. We use the details eBay already has, then ask only for what unlocks real reach."
      >
        <Badge tone="success" icon={Sparkles}>
          Estimated 3.8× audience
        </Badge>
      </PageIntro>

      <section className="registration-hero">
        <div className="registration-pitch">
          <Badge tone="dark" icon={Globe2}>
            EU Live Passport
          </Badge>
          <h2>
            You’re already ready for
            <br />
            <span>{readyCount} EU markets.</span>
          </h2>
          <p>
            Archive Trade has a strong selling record and verified business details. Confirm one
            missing detail to see your complete market reach.
          </p>
          <div className="hero-actions">
            <Button icon={ArrowRight} onClick={onContinue}>
              Build my EU Passport
            </Button>
            <Button
              variant="text-light"
              icon={Play}
              iconPosition="left"
              onClick={() => notify('A 90-second seller walkthrough would open here.')}
            >
              See how it works
            </Button>
          </div>
          <div className="value-row">
            <span>
              <Zap size={16} /> Low effort
            </span>
            <span>
              <Users size={16} /> High reach
            </span>
            <span>
              <ShieldCheck size={16} /> Sell with confidence
            </span>
          </div>
        </div>

        <div className="reach-card">
          <div className="reach-card-header">
            <span>Potential market reach</span>
            <Badge tone="success">Live estimate</Badge>
          </div>
          <div className="reach-orbit">
            <div className="orbit orbit-one" />
            <div className="orbit orbit-two" />
            <div className="seller-node">
              <Avatar label="AT" />
              <span>Amsterdam</span>
            </div>
            {euCountries.slice(0, 12).map((country, index) => (
              <span
                className={cx('country-node', `country-node-${index + 1}`)}
                key={country.code}
                title={country.name}
              >
                {country.flag}
              </span>
            ))}
          </div>
          <div className="reach-summary">
            <div>
              <strong>{readyCount}</strong>
              <span>ready now</span>
            </div>
            <div>
              <strong>{marketGroups.action.length}</strong>
              <span>one action away</span>
            </div>
            <div>
              <strong>{marketGroups.off.length}</strong>
              <span>kept off</span>
            </div>
          </div>
        </div>
      </section>

      <section className="setup-grid">
        <div className="panel setup-card">
          <SectionHeading
            eyebrow="Fast registration"
            title="Confirm, don’t re-enter"
            description="Pulled securely from your eBay business account."
          />
          <div className="confirmation-list">
            <button onClick={() => toggle('identity')} className="confirmation-row">
              <span className={cx('check-control', confirmed.identity && 'checked')}>
                {confirmed.identity && <Check size={14} />}
              </span>
              <span className="confirmation-icon">
                <BadgeCheck size={20} />
              </span>
              <span>
                <strong>Business identity</strong>
                <small>Archive Trade B.V. · Verified</small>
              </span>
              <Badge tone="success">On file</Badge>
            </button>
            <button onClick={() => toggle('origin')} className="confirmation-row">
              <span className={cx('check-control', confirmed.origin && 'checked')}>
                {confirmed.origin && <Check size={14} />}
              </span>
              <span className="confirmation-icon">
                <MapPin size={20} />
              </span>
              <span>
                <strong>Ship-from location</strong>
                <small>Amsterdam, Netherlands</small>
              </span>
              <Badge tone="success">On file</Badge>
            </button>
            <button onClick={() => toggle('returns')} className="confirmation-row">
              <span className={cx('check-control', confirmed.returns && 'checked')}>
                {confirmed.returns && <Check size={14} />}
              </span>
              <span className="confirmation-icon">
                <RotateCcw size={20} />
              </span>
              <span>
                <strong>Cross-border returns contact</strong>
                <small>Confirm who should receive EU return alerts</small>
              </span>
              <Badge tone="warning">Confirm</Badge>
            </button>
          </div>
        </div>

        <div className="panel principle-card">
          <div className="principle-icon">
            <WandSparkles size={25} />
          </div>
          <p className="eyebrow">The low-effort promise</p>
          <h3>Ask once. Reuse everywhere.</h3>
          <p>
            A single Passport powers seller, show, item and destination checks across every future
            live event.
          </p>
          <div className="reuse-flow">
            {['Seller', 'Show', 'Item', 'Destination'].map((item, index) => (
              <div key={item}>
                <span>{index + 1}</span>
                <strong>{item}</strong>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}

function EligibilityStack({ destination = 'France' }) {
  const layers = [
    {
      icon: Store,
      label: 'Seller',
      title: 'Archive Trade is approved for EU Live',
      meta: 'Identity, performance and payouts checked',
    },
    {
      icon: Radio,
      label: 'Show',
      title: 'Archive Atelier #12 is enabled',
      meta: 'Format, schedule and category checked',
    },
    {
      icon: Box,
      label: 'Item',
      title: 'Omega Seamaster can cross borders',
      meta: 'Category, origin and item specifics checked',
    },
    {
      icon: Flag,
      label: 'Destination',
      title: `${destination} is ready for this transaction`,
      meta: 'Delivery, policy and destination rules checked',
    },
  ]

  return (
    <div className="eligibility-stack">
      {layers.map(({ icon: Icon, label, title, meta }) => (
        <div className="eligibility-layer" key={label}>
          <span className="layer-icon">
            <Icon size={18} />
          </span>
          <span className="layer-label">{label}</span>
          <span className="layer-copy">
            <strong>{title}</strong>
            <small>{meta}</small>
          </span>
          <CheckCircle2 className="layer-check" size={21} />
        </div>
      ))}
    </div>
  )
}

function OnboardingScreen({ onContinue, notify }) {
  const [filter, setFilter] = useState('all')
  const [query, setQuery] = useState('')
  const [testCountry, setTestCountry] = useState('France')

  const visibleCountries = useMemo(
    () =>
      euCountries.filter(
        (country) =>
          (filter === 'all' || country.status === filter) &&
          country.name.toLowerCase().includes(query.toLowerCase()),
      ),
    [filter, query],
  )

  return (
    <>
      <PageIntro
        step={2}
        total={5}
        label="Onboarding"
        title="Your EU reach, made legible."
        description="Your Passport continuously answers one question: can this seller sell this item, in this show, to this destination?"
      >
        <Button variant="secondary" icon={Settings2} onClick={() => notify('Passport settings opened.')}>
          Passport settings
        </Button>
      </PageIntro>

      <section className="passport-summary">
        <div className="passport-identity">
          <div className="passport-seal">
            <Globe2 size={30} />
            <CheckCircle2 size={17} className="seal-check" />
          </div>
          <div>
            <p className="eyebrow">EU Live Passport</p>
            <h2>Archive Trade B.V.</h2>
            <span className="passport-meta">
              <BadgeCheck size={15} /> Verified · refreshed 3 minutes ago
            </span>
          </div>
        </div>
        <div className="passport-stat passport-stat-ready">
          <strong>{marketGroups.ready.length}</strong>
          <span>Auto-enabled</span>
          <small>Nothing to do</small>
        </div>
        <div className="passport-stat passport-stat-action">
          <strong>{marketGroups.action.length}</strong>
          <span>Need one detail</span>
          <small>Potential reach</small>
        </div>
        <div className="passport-stat passport-stat-off">
          <strong>{marketGroups.off.length}</strong>
          <span>Not enabled</span>
          <small>You stay in control</small>
        </div>
      </section>

      <section className="onboarding-grid">
        <div className="panel market-panel">
          <SectionHeading
            eyebrow="27 destinations"
            title="Market access"
            description="Every status includes a reason and the shortest path forward."
            action={<Badge tone="success" icon={CheckCircle2}>20 on</Badge>}
          />
          <div className="market-toolbar">
            <div className="filter-tabs">
              {[
                ['all', 'All', 27],
                ['ready', 'Ready', marketGroups.ready.length],
                ['action', 'Action', marketGroups.action.length],
                ['off', 'Off', marketGroups.off.length],
              ].map(([value, label, count]) => (
                <button
                  key={value}
                  className={cx(filter === value && 'active')}
                  onClick={() => setFilter(value)}
                >
                  {label} <span>{count}</span>
                </button>
              ))}
            </div>
            <label className="search-box">
              <Search size={16} />
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Find market"
              />
            </label>
          </div>
          <div className="country-grid">
            {visibleCountries.map((country) => (
              <button
                className="country-row"
                key={country.code}
                onClick={() => notify(`${country.name}: ${
                  country.status === 'ready'
                    ? 'ready for eligible items'
                    : country.status === 'action'
                      ? 'one setup action remains'
                      : 'currently kept off'
                }.`)}
              >
                <span className="country-flag">{country.flag}</span>
                <span>
                  <strong>{country.name}</strong>
                  <small>
                    {country.status === 'ready'
                      ? 'Auto-enabled'
                      : country.status === 'action'
                        ? 'Add one detail'
                        : 'Not enabled'}
                  </small>
                </span>
                <span className={cx('status-dot', `status-dot-${country.status}`)} />
                <ChevronRight size={15} />
              </button>
            ))}
          </div>
          {visibleCountries.length === 0 && (
            <div className="empty-state">No destinations match that search.</div>
          )}
        </div>

        <div className="onboarding-side">
          <div className="unlock-card">
            <div className="unlock-top">
              <span className="unlock-icon">
                <Zap size={20} fill="currentColor" />
              </span>
              <Badge tone="warning">Best next action</Badge>
            </div>
            <h3>Unlock 4 more markets</h3>
            <p>
              Confirm one cross-border returns contact. We’ll reuse it only where this detail is
              required.
            </p>
            <div className="unlock-flags">🇧🇬 🇭🇷 🇬🇷 🇷🇴</div>
            <Button
              variant="dark"
              icon={ArrowRight}
              onClick={() => notify('Setup saved. Four markets are being rechecked.')}
            >
              Add detail · 2 min
            </Button>
          </div>
          <div className="panel activity-card">
            <p className="eyebrow">Passport activity</p>
            <div className="activity-line">
              <CheckCircle2 size={17} />
              <span>
                <strong>20 markets enabled</strong>
                <small>Automatically, using verified details</small>
              </span>
              <time>Now</time>
            </div>
            <div className="activity-line">
              <ShieldCheck size={17} />
              <span>
                <strong>Seller standing checked</strong>
                <small>No action needed</small>
              </span>
              <time>3m</time>
            </div>
            <div className="activity-line">
              <LockKeyhole size={17} />
              <span>
                <strong>Sweden stays off</strong>
                <small>Your previous preference was kept</small>
              </span>
              <time>3m</time>
            </div>
          </div>
        </div>
      </section>

      <section className="panel eligibility-panel">
        <SectionHeading
          eyebrow="Eligibility, explained"
          title="Test any sale before you go live"
          description="Hard rules are resolved at four levels. A single failed layer stops exposure in that destination—without blocking the rest of your show."
          action={
            <label className="compact-select">
              <span>Destination</span>
              <select value={testCountry} onChange={(event) => setTestCountry(event.target.value)}>
                {euCountries.map((country) => (
                  <option key={country.code}>{country.name}</option>
                ))}
              </select>
            </label>
          }
        />
        <div className="eligibility-content">
          <EligibilityStack destination={testCountry} />
          <div className="decision-card">
            <div className="decision-orbit">
              <span>S</span>
              <span>SH</span>
              <span>I</span>
              <span>D</span>
              <Check size={34} strokeWidth={2.5} />
            </div>
            <Badge tone="success" icon={CheckCircle2}>
              Eligible
            </Badge>
            <h3>Yes, this sale can happen.</h3>
            <p>Omega Seamaster · Archive Atelier #12 · {testCountry}</p>
            <button onClick={() => notify('Full decision trace opened.')}>
              View decision trace <ArrowRight size={15} />
            </button>
          </div>
        </div>
      </section>

      <div className="centered-action">
        <Button icon={ArrowRight} onClick={onContinue}>
          Plan my first EU-wide show
        </Button>
      </div>
    </>
  )
}

function CatalogueTable({ notify }) {
  return (
    <div className="catalogue-table">
      <div className="catalogue-head">
        <span>Lot</span>
        <span>Starting bid</span>
        <span>EU reach</span>
        <span>Status</span>
        <span />
      </div>
      {catalogueItems.map((item) => (
        <button
          className="catalogue-row"
          key={item.id}
          onClick={() => notify(`${item.title}: item eligibility details opened.`)}
        >
          <span className="catalogue-product">
            <span className="catalogue-image" style={{ backgroundImage: `url(${item.image})` }} />
            <span>
              <strong>{item.title}</strong>
              <small>{item.subtitle}</small>
            </span>
          </span>
          <strong>{item.start}</strong>
          <span>
            <strong>{item.markets ? `${item.markets}/27` : '—'}</strong>
            <small>{item.markets ? 'destinations' : 'paused'}</small>
          </span>
          <Badge tone={item.statusType}>{item.status}</Badge>
          <ChevronRight size={17} />
        </button>
      ))}
    </div>
  )
}

function PreShowScreen({ onContinue, switchToBuyer, notify }) {
  const [localizationOn, setLocalizationOn] = useState(true)
  const [totalsOn, setTotalsOn] = useState(true)

  return (
    <>
      <PageIntro
        step={3}
        total={5}
        label="Pre-show"
        title="Plan once. Reach everywhere you’re ready."
        description="Eligibility protects the transaction. Viability makes sure the show is worth surfacing. You see both before publishing."
      >
        <Button variant="secondary" icon={Eye} onClick={switchToBuyer}>
          Preview as buyer
        </Button>
      </PageIntro>

      <section className="show-composer">
        <div className="show-cover" style={{ backgroundImage: `url(${productImages.watch})` }}>
          <Badge tone="light" icon={CalendarDays}>
            Fri 21:00 CET
          </Badge>
          <span className="show-cover-edit">Change cover</span>
        </div>
        <div className="show-main">
          <div className="show-title-row">
            <div>
              <p className="eyebrow">Draft show</p>
              <h2>Archive Atelier #12</h2>
              <p>Vintage watches, design icons & rare finds · 14 lots</p>
            </div>
            <Badge tone="warning">3 actions</Badge>
          </div>
          <div className="show-details-row">
            <span>
              <CalendarDays size={17} /> 12 September · 21:00 CET
            </span>
            <span>
              <Globe2 size={17} /> Local start times generated
            </span>
            <span>
              <Languages size={17} /> 6 caption languages
            </span>
          </div>
        </div>
        <div className="reach-score">
          <div className="score-ring">
            <strong>23</strong>
            <span>of 27</span>
          </div>
          <span>markets reached</span>
          <small>+42% likely viewers</small>
        </div>
      </section>

      <section className="pre-show-grid">
        <div className="panel catalogue-panel">
          <SectionHeading
            eyebrow="Item × destination checks"
            title="Show inventory"
            description="One restricted item never has to shrink the whole show."
            action={<Button variant="text" icon={Box}>Add lots</Button>}
          />
          <CatalogueTable notify={notify} />
          <div className="catalogue-note">
            <Info size={16} />
            <span>
              The Air Max lot is on hold because origin information is missing. The other 13 lots
              can still go live in eligible markets.
            </span>
            <button onClick={() => notify('Missing origin field opened.')}>Fix now</button>
          </div>
        </div>

        <div className="pre-show-side">
          <div className="viability-card">
            <div className="viability-header">
              <div>
                <p className="eyebrow">Viability forecast</p>
                <h3>Should we show it?</h3>
              </div>
              <span className="viability-score">84</span>
            </div>
            <Badge tone="success" icon={TrendingUp}>
              Strong EU fit
            </Badge>
            <p>
              Eligible means it <em>can</em> be shown. Viability predicts where it <em>should</em>{' '}
              be shown.
            </p>
            <div className="factor-list">
              {[
                ['Demand match', 92],
                ['Price competitiveness', 81],
                ['Delivery promise', 78],
                ['Localization coverage', 88],
              ].map(([label, score]) => (
                <div className="factor-row" key={label}>
                  <span>{label}</span>
                  <span className="factor-track">
                    <span style={{ width: `${score}%` }} />
                  </span>
                  <strong>{score}</strong>
                </div>
              ))}
            </div>
            <button onClick={() => notify('Market-by-market viability forecast opened.')}>
              Explore by market <ArrowRight size={15} />
            </button>
          </div>

          <div className="panel automation-card">
            <p className="eyebrow">Buyer-ready by default</p>
            <label className="switch-row">
              <span className="switch-icon">
                <Languages size={18} />
              </span>
              <span>
                <strong>Live localization</strong>
                <small>Titles, captions and chat</small>
              </span>
              <button
                className={cx('switch', localizationOn && 'switch-on')}
                onClick={() => setLocalizationOn((on) => !on)}
                aria-label="Toggle live localization"
              >
                <span />
              </button>
            </label>
            <label className="switch-row">
              <span className="switch-icon">
                <CircleDollarSign size={18} />
              </span>
              <span>
                <strong>All-in bid totals</strong>
                <small>Local currency, delivery and tax</small>
              </span>
              <button
                className={cx('switch', totalsOn && 'switch-on')}
                onClick={() => setTotalsOn((on) => !on)}
                aria-label="Toggle all-in bid totals"
              >
                <span />
              </button>
            </label>
          </div>
        </div>
      </section>

      <section className="publish-bar">
        <div className="publish-checks">
          <span>
            <CheckCircle2 size={18} /> Seller ready
          </span>
          <span>
            <CheckCircle2 size={18} /> 13/14 lots ready
          </span>
          <span>
            <CheckCircle2 size={18} /> 23 markets viable
          </span>
        </div>
        <Button icon={Radio} onClick={onContinue}>
          Publish EU-wide show
        </Button>
      </section>
    </>
  )
}

function SellerLiveScreen({ onContinue, switchToBuyer, notify }) {
  const translatedMessages = [
    { flag: '🇫🇷', name: 'Camille', text: 'Can you show the clasp?', source: 'French' },
    { flag: '🇩🇪', name: 'Jonas', text: 'Is the service history included?', source: 'German' },
    { flag: '🇮🇹', name: 'Luca', text: 'Beautiful dial!', source: 'Italian' },
  ]

  return (
    <>
      <PageIntro
        step={4}
        total={5}
        label="During show"
        title="One room. Everyone feels local."
        description="Localization and trust run quietly in the background, while exceptions surface only when you need to act."
      >
        <div className="live-health">
          <span className="live-dot" />
          All systems healthy
        </div>
      </PageIntro>

      <section className="seller-studio">
        <div className="studio-topbar">
          <div>
            <Badge tone="live">LIVE · 18:42</Badge>
            <strong>Archive Atelier #12</strong>
          </div>
          <div className="studio-metrics">
            <span>
              <Users size={16} /> 1,284 watching
            </span>
            <span>
              <Globe2 size={16} /> 18 markets active
            </span>
            <span>
              <Heart size={16} /> 8.6k
            </span>
          </div>
          <Button variant="studio" icon={Eye} onClick={switchToBuyer}>
            Buyer view
          </Button>
        </div>

        <div className="studio-layout">
          <div className="studio-video" style={{ backgroundImage: `url(${productImages.watch})` }}>
            <div className="camera-label">
              <span className="camera-pulse" /> Camera 1
            </div>
            <div className="caption-overlay">
              <span>
                <Languages size={14} /> Live captions · 6 languages
              </span>
              “The warm patina is completely original to this 1968 dial.”
            </div>
            <div className="lot-overlay">
              <span>LOT 07 · 00:34</span>
              <strong>Omega Seamaster 1968</strong>
              <small>Current bid · €320</small>
            </div>
          </div>

          <div className="studio-chat">
            <div className="studio-panel-title">
              <span>
                <MessageCircle size={17} /> Audience
              </span>
              <Badge tone="dark">Auto-translated</Badge>
            </div>
            <div className="chat-stream">
              {translatedMessages.map((message) => (
                <div className="chat-message" key={message.name}>
                  <span className="chat-avatar">{message.flag}</span>
                  <span>
                    <strong>{message.name}</strong>
                    <p>{message.text}</p>
                    <small>
                      <Languages size={11} /> Translated from {message.source}
                    </small>
                  </span>
                </div>
              ))}
              <div className="chat-system">
                <ShieldCheck size={15} />
                Buyer totals refreshed in 18 markets
              </div>
            </div>
            <div className="quick-reply">
              <input placeholder="Reply to everyone…" />
              <button aria-label="Send reply">
                <ArrowRight size={17} />
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="live-operations-grid">
        <div className="panel now-selling-card">
          <div className="now-selling-product">
            <div style={{ backgroundImage: `url(${productImages.watch})` }} />
            <span>
              <p className="eyebrow">Now selling · Lot 07</p>
              <h3>Omega Seamaster 1968</h3>
              <small>23 destination checks passed</small>
            </span>
          </div>
          <div className="bid-velocity">
            <span>Bid velocity</span>
            <strong>€320</strong>
            <small>12 bids · 7 bidders · 5 countries</small>
          </div>
          <div className="velocity-bars">
            {[28, 43, 31, 58, 48, 76, 64, 92, 80, 98].map((height, index) => (
              <span key={index} style={{ height: `${height}%` }} />
            ))}
          </div>
          <Button variant="dark" onClick={() => notify('Lot timer extended by 15 seconds.')}>
            +15 seconds
          </Button>
        </div>

        <div className="panel trust-monitor">
          <SectionHeading
            eyebrow="Trust monitor"
            title="18 local experiences, synchronized"
            action={<Badge tone="success">Healthy</Badge>}
          />
          <div className="monitor-grid">
            <div>
              <Languages size={19} />
              <strong>6</strong>
              <span>caption languages</span>
            </div>
            <div>
              <CircleDollarSign size={19} />
              <strong>100%</strong>
              <span>all-in totals shown</span>
            </div>
            <div>
              <Truck size={19} />
              <strong>18</strong>
              <span>delivery promises live</span>
            </div>
          </div>
          <p className="monitor-note">
            <CheckCircle2 size={15} />
            No buyer-facing eligibility errors
          </p>
        </div>

        <div className="exception-card">
          <div className="exception-heading">
            <span className="exception-icon">
              <ShieldCheck size={20} />
            </span>
            <div>
              <p className="eyebrow">Protected automatically</p>
              <h3>1 ineligible bid intercepted</h3>
            </div>
          </div>
          <p>
            A destination changed after registration. The buyer saw a clear message and your show
            continued uninterrupted.
          </p>
          <button onClick={() => notify('Eligibility exception trace opened.')}>
            View trace <ChevronRight size={15} />
          </button>
        </div>
      </section>

      <div className="centered-action">
        <Button icon={PackageCheck} onClick={onContinue}>
          End show & see fulfillment
        </Button>
      </div>
    </>
  )
}

function SellerPostShowScreen({ notify }) {
  const orders = [
    { flag: '🇫🇷', name: 'France', orders: 12, state: 'Labels ready', tone: 'success' },
    { flag: '🇩🇪', name: 'Germany', orders: 8, state: 'Labels ready', tone: 'success' },
    { flag: '🇮🇹', name: 'Italy', orders: 6, state: 'Review 1 address', tone: 'warning' },
    { flag: '🇪🇸', name: 'Spain', orders: 5, state: 'Labels ready', tone: 'success' },
  ]

  return (
    <>
      <PageIntro
        step={5}
        total={5}
        label="Post-show"
        title="The show is over. The hassle isn’t yours."
        description="Orders are grouped into one fulfillment flow. eBay generates destination-aware labels, documents and buyer updates."
      >
        <Badge tone="success" icon={CheckCircle2}>
          Show complete
        </Badge>
      </PageIntro>

      <section className="outcome-banner">
        <div>
          <p className="eyebrow">Archive Atelier #12</p>
          <h2>A strong night across Europe.</h2>
          <p>Every winning buyer saw a final total and delivery promise before paying.</p>
        </div>
        <div className="outcome-stats">
          <span>
            <strong>€8,460</strong>
            <small>sales</small>
          </span>
          <span>
            <strong>37</strong>
            <small>orders</small>
          </span>
          <span>
            <strong>9</strong>
            <small>countries</small>
          </span>
          <span>
            <strong>96%</strong>
            <small>paid</small>
          </span>
        </div>
      </section>

      <section className="post-grid">
        <div className="panel fulfillment-panel">
          <SectionHeading
            eyebrow="One fulfillment queue"
            title="Pack locally. We route globally."
            description="37 orders are grouped by the action you need to take—not by regulatory complexity."
            action={<Button variant="secondary" icon={ReceiptText}>Print all labels</Button>}
          />
          <div className="fulfillment-progress">
            <span style={{ width: '78%' }} />
          </div>
          <div className="fulfillment-progress-copy">
            <span><strong>29</strong> ready to pack</span>
            <span><strong>7</strong> awaiting payment</span>
            <span className="warning-text"><strong>1</strong> needs you</span>
          </div>
          <div className="order-groups">
            {orders.map((order) => (
              <button
                key={order.name}
                onClick={() => notify(`${order.name} fulfillment group opened.`)}
              >
                <span className="order-flag">{order.flag}</span>
                <span>
                  <strong>{order.name}</strong>
                  <small>{order.orders} orders</small>
                </span>
                <Badge tone={order.tone}>{order.state}</Badge>
                <ChevronRight size={16} />
              </button>
            ))}
          </div>
        </div>

        <div className="post-side">
          <div className="autopilot-card">
            <div className="autopilot-heading">
              <span>
                <Sparkles size={22} />
              </span>
              <div>
                <p className="eyebrow">Cross-border autopilot</p>
                <h3>52 tasks handled for you</h3>
              </div>
            </div>
            <div className="autopilot-list">
              <span><Check size={15} /> Local buyer receipts generated</span>
              <span><Check size={15} /> Destination labels prepared</span>
              <span><Check size={15} /> Tracking messages localized</span>
              <span><Check size={15} /> Returns routes attached</span>
            </div>
            <button onClick={() => notify('Autopilot activity log opened.')}>
              See everything eBay handled <ArrowRight size={15} />
            </button>
          </div>

          <div className="attention-card">
            <span className="attention-icon">
              <AlertTriangle size={20} />
            </span>
            <div>
              <p className="eyebrow">One thing needs you</p>
              <h3>Confirm an Italian address</h3>
              <p>The buyer’s apartment number may be incomplete.</p>
              <Button
                variant="dark"
                icon={ArrowRight}
                onClick={() => notify('Address confirmation request sent to buyer.')}
              >
                Review · 30 sec
              </Button>
            </div>
          </div>
        </div>
      </section>

      <section className="panel performance-panel">
        <SectionHeading
          eyebrow="Reach that compounds"
          title="What to carry into your next show"
          description="Insights are translated into concrete, reversible recommendations."
          action={<Button variant="text" icon={BarChart3}>Full report</Button>}
        />
        <div className="insight-grid">
          <div className="insight-card">
            <span className="insight-icon blue"><TrendingUp size={19} /></span>
            <div>
              <strong>France added €1,820 in sales</strong>
              <p>Your vintage watches over-indexed with French collectors.</p>
              <button onClick={() => notify('France will be prioritized next show.')}>Prioritize next time</button>
            </div>
          </div>
          <div className="insight-card">
            <span className="insight-icon yellow"><Languages size={19} /></span>
            <div>
              <strong>Captions lifted watch time 18%</strong>
              <p>German and French viewers stayed longest after localization.</p>
              <button onClick={() => notify('Localization is already enabled by default.')}>Keep enabled</button>
            </div>
          </div>
          <div className="insight-card">
            <span className="insight-icon green"><Clock3 size={19} /></span>
            <div>
              <strong>Start 30 minutes earlier</strong>
              <p>A 20:30 CET start could add an estimated 140 viewers.</p>
              <button onClick={() => notify('Next show time updated to 20:30 CET.')}>Apply to next show</button>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}

function TrustReasonCard({ destination }) {
  return (
    <div className="trust-reason-card">
      <div className="trust-reason-heading">
        <span><ShieldCheck size={20} /></span>
        <div>
          <p className="eyebrow">Why you’re seeing this</p>
          <h3>Ready for {destination.city}</h3>
        </div>
      </div>
      <div className="trust-checks">
        <span><CheckCircle2 size={16} /> Seller verified for EU Live</span>
        <span><CheckCircle2 size={16} /> Featured lots can ship to you</span>
        <span><CheckCircle2 size={16} /> Total shown before every bid</span>
        <span><CheckCircle2 size={16} /> Local returns path included</span>
      </div>
      <p className="trust-footnote">
        Eligibility is rechecked when you register, bid and pay.
      </p>
    </div>
  )
}

function BuyerDiscoveryScreen({ destination, onContinue, notify }) {
  const cards = [
    {
      title: 'Modern Icons: Milan',
      seller: 'Casa Forma',
      image: productImages.bag,
      viewers: '642',
      time: 'Live now',
      badge: 'LIVE',
    },
    {
      title: 'Rare Cameras, Vol. 4',
      seller: 'Nordlicht Foto',
      image: productImages.camera,
      viewers: '1.1k',
      time: 'Tomorrow · 19:00',
      badge: 'REMIND ME',
    },
    {
      title: 'Air & Archive',
      seller: 'Sole District',
      image: productImages.sneaker,
      viewers: '389',
      time: 'Sun · 18:30',
      badge: 'SUNDAY',
    },
  ]

  return (
    <>
      <PageIntro
        step={1}
        total={4}
        label="Discovery"
        title={`Europe’s best live finds, ready for ${destination.city}.`}
        description="Your feed includes only shows with relevant, eligible items and a trustworthy path to your door."
      >
        <Badge tone="success" icon={MapPin}>
          Localized for {destination.name}
        </Badge>
      </PageIntro>

      <section className="discovery-hero">
        <div className="featured-show" style={{ backgroundImage: `url(${productImages.watch})` }}>
          <div className="featured-shade" />
          <div className="featured-content">
            <Badge tone="live">LIVE IN 18 MIN</Badge>
            <div>
              <p className="eyebrow light">Editor’s pick · Amsterdam</p>
              <h2>Archive Atelier #12</h2>
              <p>Vintage watches, design icons and rare finds—live from the canal district.</p>
            </div>
            <div className="featured-meta">
              <span><Avatar label="AT" small /> Archive Trade <BadgeCheck size={15} /></span>
              <span><Users size={16} /> 2.4k waiting</span>
              <span><Languages size={16} /> French captions</span>
            </div>
            <div className="featured-actions">
              <Button icon={Play} onClick={onContinue}>Get ready</Button>
              <Button
                variant="glass"
                icon={Bell}
                onClick={() => notify('Reminder set for 20:55 local time.')}
              >
                Remind me
              </Button>
            </div>
          </div>
          <div className="featured-total">
            <span className="featured-total-icon"><ReceiptText size={17} /></span>
            <span>
              <small>No-surprise bidding</small>
              <strong>See your total before every bid</strong>
            </span>
            <CheckCircle2 size={18} />
          </div>
        </div>
        <TrustReasonCard destination={destination} />
      </section>

      <section className="discovery-section">
        <SectionHeading
          eyebrow="Eligible & relevant"
          title="More live rooms picked for you"
          description={`Every card has passed destination checks for ${destination.name}.`}
          action={<Button variant="text" icon={ArrowRight}>See all</Button>}
        />
        <div className="show-card-grid">
          {cards.map((card) => (
            <button className="show-card" key={card.title} onClick={onContinue}>
              <div className="show-card-image" style={{ backgroundImage: `url(${card.image})` }}>
                <Badge tone={card.badge === 'LIVE' ? 'live' : 'light'}>{card.badge}</Badge>
                <span className="save-button" onClick={(event) => {
                  event.stopPropagation()
                  notify(`${card.title} saved.`)
                }}>
                  <Heart size={17} />
                </span>
                <span className="viewer-count"><Eye size={14} /> {card.viewers}</span>
              </div>
              <div className="show-card-content">
                <div>
                  <h3>{card.title}</h3>
                  <p>{card.seller} <BadgeCheck size={13} /></p>
                </div>
                <span className="show-time">{card.time}</span>
                <div className="show-card-trust">
                  <span><Truck size={14} /> Ships to you</span>
                  <span><Languages size={14} /> Local captions</span>
                </div>
              </div>
            </button>
          ))}
        </div>
      </section>

      <section className="buyer-promise">
        <span className="buyer-promise-icon"><Globe2 size={25} /></span>
        <div>
          <p className="eyebrow">A combined EU market</p>
          <h3>Browse without doing border math.</h3>
          <p>eBay handles eligibility, localization and the delivery promise before a show reaches your feed.</p>
        </div>
        <div className="buyer-promise-points">
          <span><Check size={15} /> Relevant shows</span>
          <span><Check size={15} /> Local totals</span>
          <span><Check size={15} /> Trusted delivery</span>
        </div>
      </section>
    </>
  )
}

function BuyerPreparationScreen({ destination, onContinue, notify }) {
  const [reminder, setReminder] = useState(false)
  const startingBid = 280
  const delivery = 14.9

  return (
    <>
      <PageIntro
        step={2}
        total={4}
        label="Preparation"
        title="Know everything important before the room opens."
        description="One readiness check covers address, payment, local terms, delivery and all-in pricing."
      >
        <Badge tone="success" icon={CheckCircle2}>Ready to bid</Badge>
      </PageIntro>

      <section className="preparation-grid">
        <div className="show-detail-card">
          <div className="show-detail-image" style={{ backgroundImage: `url(${productImages.watch})` }}>
            <span className="show-countdown">
              <Clock3 size={16} /> Starts in 18:24
            </span>
            <button aria-label="Preview show" onClick={() => notify('Show trailer started.')}>
              <Play size={24} fill="currentColor" />
            </button>
          </div>
          <div className="show-detail-copy">
            <div className="seller-line">
              <Avatar label="AT" />
              <span>
                <strong>Archive Trade</strong>
                <small>Amsterdam, Netherlands · 99.8% positive</small>
              </span>
              <BadgeCheck size={20} />
            </div>
            <h2>Archive Atelier #12</h2>
            <p>Vintage watches, design icons & rare finds · 14 lots</p>
            <div className="show-detail-tags">
              <Badge tone="neutral" icon={Languages}>French captions</Badge>
              <Badge tone="neutral" icon={Truck}>3–5 business days</Badge>
              <Badge tone="neutral" icon={RotateCcw}>30-day returns</Badge>
            </div>
            <div className="show-detail-actions">
              <Button icon={Play} onClick={onContinue}>Join waiting room</Button>
              <Button
                variant={reminder ? 'success' : 'secondary'}
                icon={reminder ? Check : Bell}
                onClick={() => {
                  setReminder((set) => !set)
                  notify(reminder ? 'Reminder removed.' : 'Reminder set for 20:55 local time.')
                }}
              >
                {reminder ? 'Reminder set' : 'Remind me'}
              </Button>
            </div>
          </div>
        </div>

        <div className="ready-card">
          <div className="ready-card-top">
            <span className="ready-seal"><ShieldCheck size={25} /></span>
            <div>
              <p className="eyebrow">Bid readiness</p>
              <h3>You’re all set, Camille.</h3>
            </div>
            <Badge tone="success">4/4</Badge>
          </div>
          <div className="readiness-list">
            <button onClick={() => notify('Delivery address opened.')}>
              <span><MapPin size={18} /></span>
              <span><strong>Delivery</strong><small>{destination.city}, {destination.name}</small></span>
              <CheckCircle2 size={18} />
            </button>
            <button onClick={() => notify('Payment method opened.')}>
              <span><CircleDollarSign size={18} /></span>
              <span><strong>Payment</strong><small>Visa ending 2048</small></span>
              <CheckCircle2 size={18} />
            </button>
            <button onClick={() => notify('Buyer protection details opened.')}>
              <span><ShieldCheck size={18} /></span>
              <span><strong>Protection</strong><small>eBay Money Back Guarantee</small></span>
              <CheckCircle2 size={18} />
            </button>
            <button onClick={() => notify('Local terms opened.')}>
              <span><FileCheck2 size={18} /></span>
              <span><strong>Local terms</strong><small>Shown in your language</small></span>
              <CheckCircle2 size={18} />
            </button>
          </div>
          <p className="ready-footnote">
            <LockKeyhole size={14} /> Rechecked automatically before each bid
          </p>
        </div>
      </section>

      <section className="panel watched-lot">
        <SectionHeading
          eyebrow="Watched lot"
          title="Your price, before the pressure"
          description="Preview how a bid becomes a delivered total in your destination."
          action={<Badge tone="success" icon={CheckCircle2}>Eligible for you</Badge>}
        />
        <div className="watched-layout">
          <div className="watched-product">
            <div style={{ backgroundImage: `url(${productImages.watch})` }} />
            <span>
              <small>LOT 07</small>
              <h3>Omega Seamaster 1968</h3>
              <p>Serviced · Original dial · Seller authenticated</p>
            </span>
          </div>
          <div className="price-preview">
            <div className="price-preview-title">
              <span>If your bid wins at</span>
              <strong>{formatLocalPrice(startingBid, destination)}</strong>
            </div>
            <div className="price-line"><span>Winning bid</span><span>{formatLocalPrice(startingBid, destination)}</span></div>
            <div className="price-line"><span>Tracked delivery</span><span>{formatLocalPrice(delivery, destination)}</span></div>
            <div className="price-line muted"><span>Tax</span><span>Included</span></div>
            <div className="price-total"><span>Your delivered total</span><strong>{formatLocalPrice(startingBid + delivery, destination)}</strong></div>
            <p><ShieldCheck size={14} /> No import payment due at delivery</p>
          </div>
        </div>
      </section>

      <section className="local-time-note">
        <span><Clock3 size={21} /></span>
        <div>
          <strong>Starts at 21:00 in {destination.city}</strong>
          <small>The seller sees one CET schedule. You always see your local start time.</small>
        </div>
        <Button variant="text" onClick={() => notify('Calendar event downloaded.')}>Add to calendar</Button>
      </section>
    </>
  )
}

function BuyerLiveScreen({ destination, onContinue, notify }) {
  const [nextBid, setNextBid] = useState(340)
  const [bidPlaced, setBidPlaced] = useState(false)
  const delivery = 14.9

  const placeBid = () => {
    setBidPlaced(true)
    notify(`You’re leading at ${formatLocalPrice(nextBid, destination)}.`)
    window.setTimeout(() => {
      setNextBid((bid) => bid + 20)
      setBidPlaced(false)
    }, 1800)
  }

  return (
    <>
      <PageIntro
        step={3}
        total={4}
        label="During show"
        title="Bid in the moment. Trust what happens next."
        description="Translation, currency, delivery and protection stay visible without pulling you away from the show."
      >
        <Badge tone="live">LIVE · 18:42</Badge>
      </PageIntro>

      <section className="buyer-live-shell">
        <div className="buyer-video" style={{ backgroundImage: `url(${productImages.watch})` }}>
          <div className="buyer-video-top">
            <Badge tone="live">LIVE</Badge>
            <span><Eye size={14} /> 1,284</span>
            <span><Heart size={14} /> 8.6k</span>
          </div>
          <div className="buyer-caption">
            <span><Languages size={13} /> Translated live from English</span>
            <p>“The warm patina is completely original to this 1968 dial.”</p>
          </div>
          <div className="reaction-stream">
            <span>💙</span><span>🔥</span><span>👏</span>
          </div>
        </div>

        <div className="bid-panel">
          <div className="bid-product">
            <span>LOT 07 · 00:34</span>
            <h2>Omega Seamaster 1968</h2>
            <p>Serviced · Original dial</p>
          </div>
          <div className="current-bid">
            <span>Current bid</span>
            <strong>{formatLocalPrice(nextBid - 20, destination)}</strong>
            <small>7 bidders · Reserve met</small>
          </div>
          <div className="bid-action">
            <button className={cx('place-bid-button', bidPlaced && 'bid-success')} onClick={placeBid}>
              {bidPlaced ? (
                <><CheckCircle2 size={21} /> You’re leading</>
              ) : (
                <>Bid {formatLocalPrice(nextBid, destination)} <ArrowRight size={20} /></>
              )}
            </button>
            <div className="delivered-total">
              <span>Your total if you win</span>
              <strong>{formatLocalPrice(nextBid + delivery, destination)}</strong>
              <button onClick={() => notify('Full delivered-price breakdown opened.')} aria-label="See price breakdown">
                <Info size={14} />
              </button>
            </div>
          </div>
          <div className="bid-trust-row">
            <span><ShieldCheck size={15} /> Buyer protected</span>
            <span><Truck size={15} /> {destination.city} · 3–5 days</span>
            <span><RotateCcw size={15} /> 30-day returns</span>
          </div>
          <div className="live-chat-input">
            <input placeholder="Ask the seller…" />
            <button aria-label="Send question"><ArrowRight size={17} /></button>
          </div>
        </div>
      </section>

      <section className="live-confidence-grid">
        <div className="confidence-card">
          <div className="confidence-top">
            <span className="confidence-icon"><ShieldCheck size={22} /></span>
            <div>
              <p className="eyebrow">Bid with confidence</p>
              <h3>Everything important, still true.</h3>
            </div>
            <Badge tone="success">Live checked</Badge>
          </div>
          <div className="confidence-points">
            <button onClick={() => notify('Seller verification details opened.')}><BadgeCheck size={17} /><span><strong>Verified seller</strong><small>99.8% positive</small></span><ChevronRight size={15} /></button>
            <button onClick={() => notify('Authentication details opened.')}><Eye size={17} /><span><strong>Item as described</strong><small>Seller-authenticated</small></span><ChevronRight size={15} /></button>
            <button onClick={() => notify('Delivery promise details opened.')}><Truck size={17} /><span><strong>Tracked delivery</strong><small>Arrives 16–18 Sep</small></span><ChevronRight size={15} /></button>
          </div>
        </div>
        <div className="translation-card">
          <div>
            <span className="translation-icon"><Languages size={20} /></span>
            <div>
              <p className="eyebrow">Your room, your language</p>
              <h3>French experience</h3>
            </div>
          </div>
          <p>Seller audio remains authentic. Captions, item facts and policy language adapt to you.</p>
          <div className="language-path"><span>EN</span><ArrowRight size={15} /><span>FR</span></div>
        </div>
      </section>

      <div className="centered-action">
        <Button icon={PackageCheck} onClick={onContinue}>
          See the post-purchase journey
        </Button>
      </div>
    </>
  )
}

function BuyerPostShowScreen({ destination, notify }) {
  return (
    <>
      <PageIntro
        step={4}
        total={4}
        label="Post-show"
        title="Bought across a border. Feels like it didn’t."
        description="One local order view, one delivery promise and one support path—from payment to returns."
      >
        <Badge tone="success" icon={PackageCheck}>Paid · protected</Badge>
      </PageIntro>

      <section className="purchase-hero">
        <div className="purchase-celebration">
          <span className="purchase-check"><Check size={29} /></span>
          <p className="eyebrow">You won lot 07</p>
          <h2>It’s yours, Camille.</h2>
          <p>Your Omega Seamaster is being prepared in Amsterdam.</p>
          <div className="purchase-product">
            <div style={{ backgroundImage: `url(${productImages.watch})` }} />
            <span>
              <strong>Omega Seamaster 1968</strong>
              <small>Order 24-0912-03847</small>
            </span>
            <strong>{formatLocalPrice(354.9, destination)}</strong>
          </div>
        </div>
        <div className="delivery-promise">
          <Badge tone="success" icon={Truck}>On schedule</Badge>
          <h3>Arrives 16–18 September</h3>
          <p>{destination.city}, {destination.name}</p>
          <div className="route-line">
            <span className="route-point complete"><Store size={15} /></span>
            <span className="route-track complete" />
            <span className="route-point active"><Plane size={15} /></span>
            <span className="route-track" />
            <span className="route-point"><MapPin size={15} /></span>
          </div>
          <div className="route-labels">
            <span><strong>Packed</strong><small>Amsterdam</small></span>
            <span><strong>In transit</strong><small>Next</small></span>
            <span><strong>Delivered</strong><small>{destination.city}</small></span>
          </div>
          <Button variant="secondary" icon={ArrowRight} onClick={() => notify('Carrier tracking opened.')}>
            Track package
          </Button>
        </div>
      </section>

      <section className="post-purchase-grid">
        <div className="panel order-timeline-card">
          <SectionHeading
            eyebrow="One order journey"
            title="Updates in your language"
            description="Seller and carrier events are translated into one clear timeline."
          />
          <div className="order-timeline">
            <div className="timeline-event complete">
              <span><Check size={14} /></span>
              <div><strong>Payment confirmed</strong><small>Today · 21:48</small></div>
              <Badge tone="success">Complete</Badge>
            </div>
            <div className="timeline-event active">
              <span><PackageCheck size={15} /></span>
              <div><strong>Seller is preparing your watch</strong><small>Label and tracking are ready</small></div>
              <Badge tone="info">Now</Badge>
            </div>
            <div className="timeline-event">
              <span><Plane size={15} /></span>
              <div><strong>On the way to {destination.name}</strong><small>You’ll get a local carrier update</small></div>
            </div>
            <div className="timeline-event">
              <span><MapPin size={15} /></span>
              <div><strong>Delivery in {destination.city}</strong><small>16–18 September</small></div>
            </div>
          </div>
        </div>

        <div className="order-support-card">
          <div className="support-heading">
            <span><Headphones size={22} /></span>
            <div>
              <p className="eyebrow">One support path</p>
              <h3>Help stays local.</h3>
            </div>
          </div>
          <p>Questions, delivery issues and returns all start here—in your language.</p>
          <div className="support-actions">
            <button onClick={() => notify('Order help opened.')}><MessageCircle size={17} /><span><strong>Get order help</strong><small>Usually replies in minutes</small></span><ChevronRight size={16} /></button>
            <button onClick={() => notify('Return options opened.')}><RotateCcw size={17} /><span><strong>Return options</strong><small>Available until 18 Oct</small></span><ChevronRight size={16} /></button>
            <button onClick={() => notify('Protection details opened.')}><ShieldCheck size={17} /><span><strong>Buyer protection</strong><small>You’re covered</small></span><ChevronRight size={16} /></button>
          </div>
        </div>
      </section>

      <section className="handled-banner">
        <div className="handled-heading">
          <span><Sparkles size={24} /></span>
          <div>
            <p className="eyebrow">Quietly handled</p>
            <h3>Four borders crossed. Zero extra buyer steps.</h3>
          </div>
        </div>
        <div className="handled-list">
          <span><Check size={15} /> Eligibility</span>
          <span><Check size={15} /> Local total</span>
          <span><Check size={15} /> Seller label</span>
          <span><Check size={15} /> Tracking</span>
          <span><Check size={15} /> Returns route</span>
        </div>
      </section>
    </>
  )
}

function BlueprintDrawer({ onClose }) {
  return (
    <div className="drawer-backdrop" role="presentation" onMouseDown={onClose}>
      <aside
        className="blueprint-drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Experience logic"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="drawer-header">
          <div>
            <p className="eyebrow">North-star blueprint</p>
            <h2>One EU live market, built on earned trust.</h2>
          </div>
          <button onClick={onClose} aria-label="Close experience logic"><X size={21} /></button>
        </div>
        <p className="drawer-lede">
          Buyers should only discover what they can confidently buy. Sellers should gain reach
          without becoming cross-border operations experts.
        </p>

        <div className="drawer-section">
          <p className="drawer-label">The decision model</p>
          <div className="formula-card">
            <div className="formula-question">Can this transaction happen?</div>
            <div className="formula-parts">
              <span>Seller</span><b>×</b><span>Show</span><b>×</b><span>Item</span><b>×</b><span>Destination</span>
            </div>
            <div className="formula-arrow"><ArrowRight size={16} /></div>
            <div className="formula-outcome"><CheckCircle2 size={18} /> Eligibility</div>
          </div>
          <div className="viability-formula">
            <span><BarChart3 size={18} /></span>
            <div>
              <strong>Then: should it be shown?</strong>
              <p>Demand × price × delivery × localization = destination viability.</p>
            </div>
          </div>
        </div>

        <div className="drawer-section">
          <p className="drawer-label">Experience tenets</p>
          <div className="tenet-list">
            {experienceTenets.map((tenet) => (
              <div key={tenet.number}>
                <span>{tenet.number}</span>
                <div><strong>{tenet.title}</strong><p>{tenet.body}</p></div>
              </div>
            ))}
          </div>
        </div>

        <div className="drawer-section">
          <p className="drawer-label">The value exchange</p>
          <div className="value-exchange">
            <div>
              <span><Store size={19} /></span>
              <strong>Seller</strong>
              <p>Low effort · high reach · confidence</p>
            </div>
            <div>
              <span><ShoppingBag size={19} /></span>
              <strong>Buyer</strong>
              <p>Relevant access · local clarity · trust</p>
            </div>
          </div>
        </div>
      </aside>
    </div>
  )
}

function JourneyControls({ stages, activeIndex, onBack, onNext }) {
  const atStart = activeIndex === 0
  const atEnd = activeIndex === stages.length - 1
  return (
    <div className="journey-controls">
      <Button variant="text" icon={ArrowLeft} iconPosition="left" onClick={onBack} disabled={atStart}>
        Previous
      </Button>
      <span>
        <strong>{stages[activeIndex].label}</strong>
        <small>{activeIndex + 1} of {stages.length}</small>
      </span>
      <Button variant={atEnd ? 'secondary' : 'primary'} icon={atEnd ? Check : ArrowRight} onClick={onNext}>
        {atEnd ? 'Journey complete' : `Next: ${stages[activeIndex + 1].label}`}
      </Button>
    </div>
  )
}

function App() {
  const [role, setRole] = useState(() =>
    new URLSearchParams(window.location.search).get('role') === 'buyer' ? 'buyer' : 'seller',
  )
  const [sellerStage, setSellerStage] = useState(() => initialStageFor('seller', sellerStages.length - 1))
  const [buyerStage, setBuyerStage] = useState(() => initialStageFor('buyer', buyerStages.length - 1))
  const [destination, setDestination] = useState(destinationOptions[0])
  const [blueprintOpen, setBlueprintOpen] = useState(false)
  const [toast, setToast] = useState('')

  const stages = role === 'seller' ? sellerStages : buyerStages
  const activeIndex = role === 'seller' ? sellerStage : buyerStage
  const setActiveIndex = role === 'seller' ? setSellerStage : setBuyerStage

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    const params = new URLSearchParams()
    params.set('role', role)
    params.set('stage', String(activeIndex))
    window.history.replaceState(null, '', `${window.location.pathname}?${params.toString()}`)
  }, [role, activeIndex])

  useEffect(() => {
    if (!toast) return undefined
    const timer = window.setTimeout(() => setToast(''), 2800)
    return () => window.clearTimeout(timer)
  }, [toast])

  const notify = (message) => setToast(message)

  const next = () => {
    if (activeIndex < stages.length - 1) setActiveIndex(activeIndex + 1)
    else notify('You’ve reached the end of this journey.')
  }

  const back = () => {
    if (activeIndex > 0) setActiveIndex(activeIndex - 1)
  }

  const switchToBuyer = (stage = 1) => {
    setRole('buyer')
    setBuyerStage(stage)
  }

  const renderSellerScreen = () => {
    switch (sellerStage) {
      case 0:
        return <RegistrationScreen onContinue={() => setSellerStage(1)} notify={notify} />
      case 1:
        return <OnboardingScreen onContinue={() => setSellerStage(2)} notify={notify} />
      case 2:
        return (
          <PreShowScreen
            onContinue={() => setSellerStage(3)}
            switchToBuyer={() => switchToBuyer(1)}
            notify={notify}
          />
        )
      case 3:
        return (
          <SellerLiveScreen
            onContinue={() => setSellerStage(4)}
            switchToBuyer={() => switchToBuyer(2)}
            notify={notify}
          />
        )
      default:
        return <SellerPostShowScreen notify={notify} />
    }
  }

  const renderBuyerScreen = () => {
    switch (buyerStage) {
      case 0:
        return (
          <BuyerDiscoveryScreen
            destination={destination}
            onContinue={() => setBuyerStage(1)}
            notify={notify}
          />
        )
      case 1:
        return (
          <BuyerPreparationScreen
            destination={destination}
            onContinue={() => setBuyerStage(2)}
            notify={notify}
          />
        )
      case 2:
        return (
          <BuyerLiveScreen
            destination={destination}
            onContinue={() => setBuyerStage(3)}
            notify={notify}
          />
        )
      default:
        return <BuyerPostShowScreen destination={destination} notify={notify} />
    }
  }

  return (
    <div className="app-shell">
      <AppHeader
        role={role}
        onRoleChange={setRole}
        destination={destination}
        onDestinationChange={setDestination}
        onOpenBlueprint={() => setBlueprintOpen(true)}
      />
      <StageNav role={role} stages={stages} activeIndex={activeIndex} onSelect={setActiveIndex} />
      <main className="main-content">
        {role === 'seller' ? renderSellerScreen() : renderBuyerScreen()}
        <JourneyControls
          stages={stages}
          activeIndex={activeIndex}
          onBack={back}
          onNext={next}
        />
      </main>
      <footer className="concept-footer">
        <div>
          <EbayLogo />
          <span>EU Live · Experience concept</span>
        </div>
        <p>Low effort, high reach for sellers. Relevant access and trust for buyers.</p>
      </footer>
      {blueprintOpen && <BlueprintDrawer onClose={() => setBlueprintOpen(false)} />}
      <div className={cx('toast', toast && 'toast-visible')} role="status">
        <CheckCircle2 size={18} />
        {toast}
      </div>
    </div>
  )
}

export default App
