interface PriceTier {
  label: string;
  budget: string;
  price: string;
}

const tiers: PriceTier[] = [
  { label: 'Small', budget: 'Under $1M budget', price: '$350' },
  { label: 'Mid', budget: '$1M – $5M budget', price: '$650' },
  { label: 'Large', budget: 'Over $5M budget', price: '$950' },
];

const compareRows = [
  {
    label: 'Cost',
    before: '$2,500+ consulting project',
    after: 'Flat project rate',
  },
  {
    label: 'Board time',
    before: '25+ hours from your volunteer board',
    after: 'Board stays focused on governance',
  },
  {
    label: 'What you inherit',
    before: 'Broken CRM. Disorganized files. No stakeholder visits.',
    after: 'Organized research, filed and ready',
  },
  {
    label: 'What you get',
    before: 'Advice and a theory',
    after: 'An action plan — then we get out of the way',
  },
];

export default function Pricing() {
  return (
    <section className="max-w-[1120px] mx-auto px-[1.4rem] py-[3.2rem] border-t border-brand-stone">
      <h2 className="font-fraunces text-[1.7rem] font-semibold text-brand-green mb-6">
        What it costs
      </h2>

      {/* Comparison table */}
      <div className="overflow-x-auto mb-8">
        <table className="w-full max-w-[640px] text-[0.9rem] border-collapse">
          <thead>
            <tr>
              <th className="text-left py-2 pr-6 text-brand-slate/50 font-medium text-[0.8rem] uppercase tracking-wide w-[110px]" />
              <th className="text-left py-2 pr-6 text-brand-slate/50 font-medium text-[0.8rem] uppercase tracking-wide">
                Without GroundWork
              </th>
              <th className="text-left py-2 text-brand-green font-semibold text-[0.8rem] uppercase tracking-wide">
                With GroundWork
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-brand-stone">
            {compareRows.map((row) => (
              <tr key={row.label}>
                <td className="py-3.5 pr-6 text-[0.78rem] text-brand-slate/50 font-medium align-top">
                  {row.label}
                </td>
                <td className="py-3.5 pr-6 align-top">
                  <span className="line-through decoration-brand-clay/70 text-brand-slate/50">
                    {row.before}
                  </span>
                </td>
                <td className="py-3.5 align-top font-medium text-brand-green">{row.after}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Package pricing */}
      <h3 className="font-fraunces text-[1.1rem] font-semibold text-brand-green mb-3">
        Flat, project-based pricing
      </h3>
      <div className="max-w-[480px] divide-y divide-brand-stone border border-brand-stone rounded-[10px] overflow-hidden bg-white mb-4">
        {tiers.map((tier) => (
          <div key={tier.label} className="flex items-center justify-between px-5 py-3.5">
            <div>
              <span className="font-semibold text-brand-green text-[0.95rem]">{tier.label}</span>
              <span className="text-[0.82rem] text-brand-slate/60 ml-2">{tier.budget}</span>
            </div>
            <span className="font-fraunces text-[1.3rem] font-bold text-brand-green">{tier.price}</span>
          </div>
        ))}
        <div className="px-5 py-3 bg-brand-bg text-[0.82rem] text-brand-slate/70">
          A <strong className="text-brand-slate">$150 deposit</strong> starts the project and applies to your total. Executive roles start at $500.
        </div>
      </div>

      {/* Scope / differentiation */}
      <div className="mt-8 max-w-[580px] border border-brand-stone rounded-[10px] bg-white p-5">
        <p className="text-[0.85rem] font-semibold text-brand-green uppercase tracking-wide mb-2">Who we work alongside</p>
        <p className="text-[0.93rem] leading-relaxed">
          Our specific scope — role readiness and pre-hire groundwork — means we work alongside{' '}
          <strong>fractional leaders</strong> and <strong>executive search firms</strong> without
          overlap. We're not placement. We're preparation. And we're built for organizations that
          need real deliverables at a price that doesn't require a board vote.
        </p>
      </div>
    </section>
  );
}
