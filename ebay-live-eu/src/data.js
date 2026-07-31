export const sellerStages = [
  { id: 'register', label: 'Register', short: '01', helper: 'Spring invitation' },
  { id: 'onboarding', label: 'EU Passport', short: '02', helper: 'Onboarding' },
  { id: 'pre-show', label: 'Plan show', short: '03', helper: 'Pre-show' },
  { id: 'live', label: 'Go live', short: '04', helper: 'During show' },
  { id: 'post-show', label: 'Fulfil', short: '05', helper: 'Post-show' },
]

export const buyerStages = [
  { id: 'discovery', label: 'Discover', short: '01', helper: 'Relevant to you' },
  { id: 'preparation', label: 'Get ready', short: '02', helper: 'Preparation' },
  { id: 'live', label: 'Join live', short: '03', helper: 'During show' },
  { id: 'post-show', label: 'Track order', short: '04', helper: 'Post-show' },
]

export const euCountries = [
  { name: 'Austria', code: 'AT', flag: '🇦🇹', status: 'ready' },
  { name: 'Belgium', code: 'BE', flag: '🇧🇪', status: 'ready' },
  { name: 'Bulgaria', code: 'BG', flag: '🇧🇬', status: 'action' },
  { name: 'Croatia', code: 'HR', flag: '🇭🇷', status: 'action' },
  { name: 'Cyprus', code: 'CY', flag: '🇨🇾', status: 'off' },
  { name: 'Czechia', code: 'CZ', flag: '🇨🇿', status: 'ready' },
  { name: 'Denmark', code: 'DK', flag: '🇩🇰', status: 'ready' },
  { name: 'Estonia', code: 'EE', flag: '🇪🇪', status: 'ready' },
  { name: 'Finland', code: 'FI', flag: '🇫🇮', status: 'ready' },
  { name: 'France', code: 'FR', flag: '🇫🇷', status: 'ready' },
  { name: 'Germany', code: 'DE', flag: '🇩🇪', status: 'ready' },
  { name: 'Greece', code: 'GR', flag: '🇬🇷', status: 'action' },
  { name: 'Hungary', code: 'HU', flag: '🇭🇺', status: 'ready' },
  { name: 'Ireland', code: 'IE', flag: '🇮🇪', status: 'ready' },
  { name: 'Italy', code: 'IT', flag: '🇮🇹', status: 'ready' },
  { name: 'Latvia', code: 'LV', flag: '🇱🇻', status: 'ready' },
  { name: 'Lithuania', code: 'LT', flag: '🇱🇹', status: 'ready' },
  { name: 'Luxembourg', code: 'LU', flag: '🇱🇺', status: 'ready' },
  { name: 'Malta', code: 'MT', flag: '🇲🇹', status: 'off' },
  { name: 'Netherlands', code: 'NL', flag: '🇳🇱', status: 'ready' },
  { name: 'Poland', code: 'PL', flag: '🇵🇱', status: 'ready' },
  { name: 'Portugal', code: 'PT', flag: '🇵🇹', status: 'ready' },
  { name: 'Romania', code: 'RO', flag: '🇷🇴', status: 'action' },
  { name: 'Slovakia', code: 'SK', flag: '🇸🇰', status: 'ready' },
  { name: 'Slovenia', code: 'SI', flag: '🇸🇮', status: 'ready' },
  { name: 'Spain', code: 'ES', flag: '🇪🇸', status: 'ready' },
  { name: 'Sweden', code: 'SE', flag: '🇸🇪', status: 'off' },
]

export const destinationOptions = [
  { name: 'France', code: 'FR', flag: '🇫🇷', city: 'Paris', currency: '€' },
  { name: 'Germany', code: 'DE', flag: '🇩🇪', city: 'Berlin', currency: '€' },
  { name: 'Italy', code: 'IT', flag: '🇮🇹', city: 'Milan', currency: '€' },
  { name: 'Poland', code: 'PL', flag: '🇵🇱', city: 'Warsaw', currency: 'zł' },
  { name: 'Sweden', code: 'SE', flag: '🇸🇪', city: 'Stockholm', currency: 'kr' },
]

export const productImages = {
  watch:
    'https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1200&q=85',
  bag:
    'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=1200&q=85',
  sneaker:
    'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=85',
  camera:
    'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1200&q=85',
}

export const marketGroups = {
  ready: euCountries.filter((country) => country.status === 'ready'),
  action: euCountries.filter((country) => country.status === 'action'),
  off: euCountries.filter((country) => country.status === 'off'),
}

export const catalogueItems = [
  {
    id: '01',
    title: 'Omega Seamaster 1968',
    subtitle: 'Ref. 166.032 · Serviced',
    image: productImages.watch,
    markets: 23,
    status: 'Ready',
    statusType: 'success',
    start: '€280',
  },
  {
    id: '02',
    title: 'Celine Triomphe bag',
    subtitle: 'Tan calfskin · Excellent',
    image: productImages.bag,
    markets: 21,
    status: '1 detail',
    statusType: 'warning',
    start: '€410',
  },
  {
    id: '03',
    title: 'Air Max 1 “Chlorophyll”',
    subtitle: 'EU 43 · New in box',
    image: productImages.sneaker,
    markets: 0,
    status: 'Hold',
    statusType: 'danger',
    start: '€165',
  },
  {
    id: '04',
    title: 'Leica M6 Classic',
    subtitle: 'Black chrome · 0.72',
    image: productImages.camera,
    markets: 23,
    status: 'Ready',
    statusType: 'success',
    start: '€1,900',
  },
]

export const experienceTenets = [
  {
    number: '01',
    title: 'Earn the exposure',
    body: 'Eligibility is resolved before a show or item appears to a buyer.',
  },
  {
    number: '02',
    title: 'Automate the happy path',
    body: 'Use trusted eBay data first; ask once, only when an answer unlocks reach.',
  },
  {
    number: '03',
    title: 'No surprise totals',
    body: 'Every buyer sees a local, landed total before committing to a bid.',
  },
  {
    number: '04',
    title: 'Explain every boundary',
    body: 'A seller can see what is on, what is off, why, and the next best action.',
  },
  {
    number: '05',
    title: 'Local by default',
    body: 'Language, currency, delivery, support and policy adapt to destination.',
  },
]
