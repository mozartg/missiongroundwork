export default function Bio() {
  const credentials = [
    'Former Caseworker to Executive Director',
    'City and Government Implementor',
    'Social Worker with Clinical and Organizational Background',
    'Grassroots Fundraising and Special Events',
    'Program Leadership and Startups',
  ];

  return (
    <section className="max-w-[1120px] mx-auto px-[1.4rem] py-[3.2rem] border-t border-brand-stone">
      <h2 className="font-fraunces text-[1.7rem] font-semibold text-brand-green mb-5">
        Who's behind it
      </h2>

      <div className="flex flex-col sm:flex-row gap-8 max-w-[700px]">
        <ul className="space-y-2 shrink-0">
          {credentials.map((c) => (
            <li key={c} className="flex items-start gap-2.5 text-[0.9rem]">
              <span className="w-1.5 h-1.5 rounded-full bg-brand-green mt-[0.45em] shrink-0" />
              {c}
            </li>
          ))}
        </ul>
      </div>

      <p className="mt-6 max-w-[62ch] text-[0.97rem] leading-relaxed">
        Mozart (Mo) Guerrier has led, advised, and rebuilt mission-driven organizations. Mission
        Groundwork exists because new hires and new leaders lose their first months reconstructing
        what should already exist. We lay the groundwork so you can focus on serving now, not later.
      </p>

      <p className="mt-3 text-[0.9rem]">
        Connect on{' '}
        <a
          href="https://linkedin.com/in/mozartg"
          target="_blank"
          rel="noopener noreferrer"
          className="text-brand-green underline underline-offset-2 hover:text-brand-green-dark transition-colors"
        >
          LinkedIn
        </a>
        .
      </p>

      {/* Partnership */}
      <div className="mt-8 border-t border-brand-stone pt-6 max-w-[600px]">
        <h3 className="font-fraunces text-[1rem] font-semibold text-brand-green mb-2">
          Working with partners
        </h3>
        <p className="text-[0.93rem] leading-relaxed">
          We partner with HR firms, executive search firms, and staffing agencies. We provide
          partnership and referrals, not placement or recruiting. The hire is yours — the
          groundwork is where we thrive.
        </p>
      </div>
    </section>
  );
}
