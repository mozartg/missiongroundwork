export default function Header() {
  return (
    <header className="max-w-[1180px] mx-auto px-5 md:px-8 py-5">
      <div className="flex items-center justify-between gap-6 rounded-2xl border border-brand-green/10 bg-white/85 px-4 py-3 shadow-sm backdrop-blur md:px-6">
        <a href="#top" className="inline-flex items-baseline no-underline" aria-label="Mission GroundWork home">
          <span className="font-fraunces text-xl md:text-2xl text-brand-green font-semibold tracking-[-0.02em]">
            Mission Ground<span className="text-brand-clay">Work</span>
          </span>
        </a>

        <nav className="hidden items-center gap-6 text-sm font-medium text-brand-slate md:flex" aria-label="Primary navigation">
          <a href="#process" className="hover:text-brand-green">How it works</a>
          <a href="#lanes" className="hover:text-brand-green">Plans</a>
          <a href="#pricing" className="hover:text-brand-green">Pricing</a>
          <a href="#about" className="hover:text-brand-green">About</a>
        </nav>

        <a
          href="#contact"
          className="rounded-full bg-brand-green px-4 py-2.5 text-sm font-semibold text-white no-underline transition hover:bg-brand-green-dark focus:outline-none focus:ring-2 focus:ring-brand-clay focus:ring-offset-2"
        >
          Build my groundwork
        </a>
      </div>
    </header>
  );
}