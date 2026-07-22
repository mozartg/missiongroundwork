import { ArrowRight, Check, FileCheck2, Layers3, Route } from 'lucide-react';

const signals = [
  { icon: FileCheck2, label: 'Role-ready plans' },
  { icon: Layers3, label: 'Usable operating artifacts' },
  { icon: Route, label: 'Handoff-ready systems' },
];

const planItems = [
  ['First 30 days', 'Priorities, decisions, and working cadence'],
  ['Core artifacts', 'SOPs, maps, calendars, and baselines'],
  ['Clean handoff', 'Owners, next actions, and measures'],
];

export default function Hero() {
  return (
    <section id="top" className="max-w-[1180px] mx-auto px-5 md:px-8 pt-8 pb-16 md:pt-14 md:pb-24">
      <div className="grid items-center gap-12 lg:grid-cols-[1.08fr_.92fr]">
        <div>
          <p className="mb-5 inline-flex rounded-full border border-brand-clay/30 bg-white px-3.5 py-2 text-xs font-bold uppercase tracking-[0.16em] text-brand-green shadow-sm">
            Implementation support for lean nonprofit teams
          </p>

          <h1 className="font-fraunces text-[clamp(2.65rem,6vw,5.25rem)] leading-[0.98] font-semibold tracking-[-0.045em] text-brand-green max-w-[13ch]">
            Start the work before the new hire starts.
          </h1>

          <p className="mt-7 max-w-[61ch] text-lg leading-8 text-brand-slate md:text-xl">
            Mission GroundWork turns an urgent role, program, or transition into a practical launch system—so your next leader inherits priorities, tools, and a clear first move instead of a blank page.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <a
              href="#contact"
              className="inline-flex items-center justify-center gap-2 rounded-full bg-brand-green px-6 py-3.5 font-semibold text-white no-underline transition hover:bg-brand-green-dark focus:outline-none focus:ring-2 focus:ring-brand-clay focus:ring-offset-2"
            >
              Build my groundwork <ArrowRight size={18} />
            </a>
            <a
              href="#process"
              className="inline-flex items-center justify-center rounded-full border border-brand-green/20 bg-white px-6 py-3.5 font-semibold text-brand-green no-underline transition hover:border-brand-green/40 hover:bg-white/70"
            >
              See the working method
            </a>
          </div>

          <div className="mt-9 grid gap-3 sm:grid-cols-3" aria-label="GroundWork operating signals">
            {signals.map(({ icon: Icon, label }) => (
              <div key={label} className="flex items-center gap-2 rounded-xl border border-brand-green/10 bg-white/70 px-3 py-3 text-sm font-semibold text-brand-slate">
                <Icon size={17} className="text-brand-clay" aria-hidden="true" />
                <span>{label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="relative">
          <div className="absolute -inset-5 -z-10 rounded-[2.5rem] bg-brand-clay/10 blur-2xl" />
          <div className="overflow-hidden rounded-[2rem] border border-brand-green/10 bg-brand-green p-5 shadow-2xl shadow-brand-green/15 md:p-7">
            <div className="flex items-center justify-between border-b border-white/15 pb-5">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/60">Example output</p>
                <h2 className="mt-1 font-fraunces text-2xl font-semibold text-white">GroundWork Plan</h2>
              </div>
              <span className="rounded-full bg-brand-clay px-3 py-1.5 text-xs font-bold text-white">READY</span>
            </div>

            <div className="mt-5 space-y-3">
              {planItems.map(([title, description], index) => (
                <div key={title} className="rounded-2xl bg-white p-4 md:p-5">
                  <div className="flex gap-3">
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-brand-clay/15 text-xs font-bold text-brand-clay">0{index + 1}</span>
                    <div>
                      <h3 className="font-semibold text-brand-green">{title}</h3>
                      <p className="mt-1 text-sm leading-6 text-brand-slate">{description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-5 flex items-start gap-3 rounded-2xl border border-white/15 bg-white/10 p-4 text-sm leading-6 text-white/90">
              <Check size={18} className="mt-0.5 shrink-0 text-brand-clay" aria-hidden="true" />
              <p>No theory deck left on a shelf. Every engagement ends with owned actions and working materials.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}