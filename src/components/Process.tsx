interface Lane {
  title: string;
  forLine: string;
  caption: string;
  svg: React.ReactNode;
}

const lanes: Lane[] = [
  {
    title: 'Executive GroundWork',
    forLine: 'For boards taking on a new executive director',
    caption: 'Every relationship has an owner and a last touch. Your new exec knows who to call and when.',
    svg: (
      <svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" aria-label="Stakeholder map sample" className="w-full h-auto rounded-md border border-brand-stone block">
        <rect x={0} y={0} width={400} height={34} fill="#2E5E4E" />
        <text x={14} y={22} fontFamily="Georgia,serif" fontSize={13} fill="#F7F5F2">Stakeholder Map — Riverbend Community Fund</text>
        <text x={386} y={22} fontFamily="Arial" fontSize={8} fill="#D9CDBA" textAnchor="end" letterSpacing={2}>SAMPLE</text>
        <circle cx={200} cy={140} r={34} fill="#2E5E4E" />
        <text x={200} y={137} fontFamily="Arial" fontSize={10} fill="#F7F5F2" textAnchor="middle">Incoming</text>
        <text x={200} y={149} fontFamily="Arial" fontSize={10} fill="#F7F5F2" textAnchor="middle">Director</text>
        <line x1={200} y1={140} x2={80} y2={80} stroke="#D9CDBA" strokeWidth={1.5} />
        <line x1={200} y1={140} x2={320} y2={80} stroke="#D9CDBA" strokeWidth={1.5} />
        <line x1={200} y1={140} x2={80} y2={205} stroke="#D9CDBA" strokeWidth={1.5} />
        <line x1={200} y1={140} x2={320} y2={205} stroke="#D9CDBA" strokeWidth={1.5} />
        <line x1={200} y1={140} x2={200} y2={60} stroke="#D9CDBA" strokeWidth={1.5} />
        <circle cx={80} cy={80} r={26} fill="#F7F5F2" stroke="#2E5E4E" />
        <text x={80} y={78} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Meyer</text>
        <text x={80} y={89} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Foundation</text>
        <circle cx={320} cy={80} r={26} fill="#F7F5F2" stroke="#2E5E4E" />
        <text x={320} y={78} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Board</text>
        <text x={320} y={89} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">President</text>
        <circle cx={200} cy={60} r={22} fill="#F7F5F2" stroke="#A86E4A" />
        <text x={200} y={58} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">City</text>
        <text x={200} y={69} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Partners</text>
        <circle cx={80} cy={205} r={26} fill="#F7F5F2" stroke="#2E5E4E" />
        <text x={80} y={203} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Program</text>
        <text x={80} y={214} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Leads</text>
        <circle cx={320} cy={205} r={26} fill="#F7F5F2" stroke="#2E5E4E" />
        <text x={320} y={203} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Major</text>
        <text x={320} y={214} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Donors</text>
        <text x={14} y={250} fontFamily="Arial" fontSize={8} fill="#39434D" opacity={0.7}>22 relationships mapped · owner and last contact noted for each</text>
      </svg>
    ),
  },
  {
    title: 'Development GroundWork',
    forLine: 'For your incoming fundraising hire',
    caption: 'Twelve months of deadlines, pre‑calendared. Your fundraiser walks in with a running start.',
    svg: (
      <svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" aria-label="Grant deadline calendar sample" className="w-full h-auto rounded-md border border-brand-stone block">
        <rect x={0} y={0} width={400} height={34} fill="#2E5E4E" />
        <text x={14} y={22} fontFamily="Georgia,serif" fontSize={13} fill="#F7F5F2">Grant Deadline Calendar — next 12 months</text>
        <text x={386} y={22} fontFamily="Arial" fontSize={8} fill="#D9CDBA" textAnchor="end" letterSpacing={2}>SAMPLE</text>
        <text x={14} y={56} fontFamily="Arial" fontSize={9} fill="#A86E4A" fontWeight="bold">DATE</text>
        <text x={80} y={56} fontFamily="Arial" fontSize={9} fill="#A86E4A" fontWeight="bold">FUNDER</text>
        <text x={240} y={56} fontFamily="Arial" fontSize={9} fill="#A86E4A" fontWeight="bold">TYPE</text>
        <text x={330} y={56} fontFamily="Arial" fontSize={9} fill="#A86E4A" fontWeight="bold">ASK</text>
        <line x1={14} y1={64} x2={386} y2={64} stroke="#D9CDBA" strokeWidth={1} />
        <text x={14} y={80} fontFamily="Arial" fontSize={10} fill="#39434D">Aug 15</text>
        <text x={80} y={80} fontFamily="Arial" fontSize={10} fill="#39434D">Hartwell Family Fund</text>
        <text x={240} y={80} fontFamily="Arial" fontSize={10} fill="#39434D">Renewal</text>
        <text x={330} y={80} fontFamily="Arial" fontSize={10} fill="#39434D">$25,000</text>
        <line x1={14} y1={96} x2={386} y2={96} stroke="#D9CDBA" strokeWidth={1} />
        <text x={14} y={112} fontFamily="Arial" fontSize={10} fill="#39434D">Sep 1</text>
        <text x={80} y={112} fontFamily="Arial" fontSize={10} fill="#39434D">State arts council</text>
        <text x={240} y={112} fontFamily="Arial" fontSize={10} fill="#39434D">New</text>
        <text x={330} y={112} fontFamily="Arial" fontSize={10} fill="#39434D">$40,000</text>
        <line x1={14} y1={128} x2={386} y2={128} stroke="#D9CDBA" strokeWidth={1} />
        <text x={14} y={144} fontFamily="Arial" fontSize={10} fill="#39434D">Sep 30</text>
        <text x={80} y={144} fontFamily="Arial" fontSize={10} fill="#39434D">Meyer Foundation</text>
        <text x={240} y={144} fontFamily="Arial" fontSize={10} fill="#39434D">Report due</text>
        <text x={330} y={144} fontFamily="Arial" fontSize={10} fill="#39434D">—</text>
        <line x1={14} y1={160} x2={386} y2={160} stroke="#D9CDBA" strokeWidth={1} />
        <text x={14} y={176} fontFamily="Arial" fontSize={10} fill="#39434D">Oct 15</text>
        <text x={80} y={176} fontFamily="Arial" fontSize={10} fill="#39434D">Community foundation</text>
        <text x={240} y={176} fontFamily="Arial" fontSize={10} fill="#39434D">New</text>
        <text x={330} y={176} fontFamily="Arial" fontSize={10} fill="#39434D">$15,000</text>
        <rect x={14} y={198} width={372} height={24} rx={4} fill="#F7F5F2" />
        <text x={24} y={214} fontFamily="Arial" fontSize={9} fill="#2E5E4E">14 deadlines calendared · reminders set 60 and 30 days out</text>
      </svg>
    ),
  },
  {
    title: 'Program GroundWork',
    forLine: 'For your incoming program leader',
    caption: 'Prior‑year results, pulled into one page. Your new lead has a baseline, not a scavenger hunt.',
    svg: (
      <svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" aria-label="Prior-year results sample" className="w-full h-auto rounded-md border border-brand-stone block">
        <rect x={0} y={0} width={400} height={34} fill="#2E5E4E" />
        <text x={14} y={22} fontFamily="Georgia,serif" fontSize={13} fill="#F7F5F2">Prior-Year Results — program summary</text>
        <text x={386} y={22} fontFamily="Arial" fontSize={8} fill="#D9CDBA" textAnchor="end" letterSpacing={2}>SAMPLE</text>
        <text x={14} y={64} fontFamily="Arial" fontSize={10} fill="#39434D">Families served</text>
        <rect x={140} y={53} width={176} height={14} rx={3} fill="#2E5E4E" opacity={0.85} />
        <text x={322} y={64} fontFamily="Arial" fontSize={10} fill="#A86E4A" fontWeight="bold">412</text>
        <text x={14} y={102} fontFamily="Arial" fontSize={10} fill="#39434D">Workshops held</text>
        <rect x={140} y={91} width={120} height={14} rx={3} fill="#2E5E4E" opacity={0.85} />
        <text x={266} y={102} fontFamily="Arial" fontSize={10} fill="#A86E4A" fontWeight="bold">36</text>
        <text x={14} y={140} fontFamily="Arial" fontSize={10} fill="#39434D">Partner referrals</text>
        <rect x={140} y={129} width={90} height={14} rx={3} fill="#2E5E4E" opacity={0.85} />
        <text x={236} y={140} fontFamily="Arial" fontSize={10} fill="#A86E4A" fontWeight="bold">128</text>
        <text x={14} y={178} fontFamily="Arial" fontSize={10} fill="#39434D">Volunteer hours</text>
        <rect x={140} y={167} width={144} height={14} rx={3} fill="#2E5E4E" opacity={0.85} />
        <text x={290} y={178} fontFamily="Arial" fontSize={10} fill="#A86E4A" fontWeight="bold">2,940</text>
        <text x={14} y={222} fontFamily="Arial" fontSize={8} fill="#39434D" opacity={0.7}>Collected from staff interviews and existing reports · unknowns marked "not tracked"</text>
      </svg>
    ),
  },
  {
    title: 'Communications GroundWork',
    forLine: 'For your incoming communications hire',
    caption: "A week of posts, already approved. Your new hire publishes before they've finished setting up their email.",
    svg: (
      <svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" aria-label="Content calendar sample" className="w-full h-auto rounded-md border border-brand-stone block">
        <rect x={0} y={0} width={400} height={34} fill="#2E5E4E" />
        <text x={14} y={22} fontFamily="Georgia,serif" fontSize={13} fill="#F7F5F2">Content Calendar — week one, pre-approved</text>
        <text x={386} y={22} fontFamily="Arial" fontSize={8} fill="#D9CDBA" textAnchor="end" letterSpacing={2}>SAMPLE</text>
        <rect x={14} y={48} width={36} height={20} rx={4} fill="#F7F5F2" stroke="#D9CDBA" />
        <text x={32} y={62} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Mon</text>
        <text x={60} y={62} fontFamily="Arial" fontSize={10} fill="#39434D">Client story: Maria finds housing</text>
        <rect x={310} y={49} width={76} height={18} rx={9} fill="#2E5E4E" />
        <text x={348} y={62} fontFamily="Arial" fontSize={8} fill="#F7F5F2" textAnchor="middle">APPROVED</text>
        <rect x={14} y={86} width={36} height={20} rx={4} fill="#F7F5F2" stroke="#D9CDBA" />
        <text x={32} y={100} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Wed</text>
        <text x={60} y={100} fontFamily="Arial" fontSize={10} fill="#39434D">Volunteer spotlight</text>
        <rect x={310} y={87} width={76} height={18} rx={9} fill="#2E5E4E" />
        <text x={348} y={100} fontFamily="Arial" fontSize={8} fill="#F7F5F2" textAnchor="middle">APPROVED</text>
        <rect x={14} y={124} width={36} height={20} rx={4} fill="#F7F5F2" stroke="#D9CDBA" />
        <text x={32} y={138} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Fri</text>
        <text x={60} y={138} fontFamily="Arial" fontSize={10} fill="#39434D">Program update: fall enrollment</text>
        <rect x={310} y={125} width={76} height={18} rx={9} fill="#2E5E4E" />
        <text x={348} y={138} fontFamily="Arial" fontSize={8} fill="#F7F5F2" textAnchor="middle">APPROVED</text>
        <rect x={14} y={162} width={36} height={20} rx={4} fill="#F7F5F2" stroke="#D9CDBA" />
        <text x={32} y={176} fontFamily="Arial" fontSize={9} fill="#39434D" textAnchor="middle">Mon</text>
        <text x={60} y={176} fontFamily="Arial" fontSize={10} fill="#39434D">Donor thank-you feature</text>
        <rect x={310} y={163} width={76} height={18} rx={9} fill="#A86E4A" />
        <text x={348} y={176} fontFamily="Arial" fontSize={8} fill="#F7F5F2" textAnchor="middle">DRAFTED</text>
        <text x={14} y={218} fontFamily="Arial" fontSize={8} fill="#39434D" opacity={0.7}>12 posts written · voice-matched · ED sign-off documented per post</text>
      </svg>
    ),
  },
  {
    title: 'Operations GroundWork',
    forLine: 'For your incoming operations hire',
    caption: "Step‑by‑step procedures, documented from the people who do the work. Nothing lives in someone's head anymore.",
    svg: (
      <svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" aria-label="SOP sample" className="w-full h-auto rounded-md border border-brand-stone block">
        <rect x={0} y={0} width={400} height={34} fill="#2E5E4E" />
        <text x={14} y={22} fontFamily="Georgia,serif" fontSize={13} fill="#F7F5F2">Standard Operating Procedure — gift processing</text>
        <text x={386} y={22} fontFamily="Arial" fontSize={8} fill="#D9CDBA" textAnchor="end" letterSpacing={2}>SAMPLE</text>
        <circle cx={26} cy={58} r={10} fill="#2E5E4E" />
        <text x={26} y={62} fontFamily="Arial" fontSize={10} fill="#F7F5F2" textAnchor="middle">1</text>
        <text x={46} y={62} fontFamily="Arial" fontSize={10} fill="#39434D">Export donor list from CRM every Friday</text>
        <circle cx={26} cy={94} r={10} fill="#2E5E4E" />
        <text x={26} y={98} fontFamily="Arial" fontSize={10} fill="#F7F5F2" textAnchor="middle">2</text>
        <text x={46} y={98} fontFamily="Arial" fontSize={10} fill="#39434D">Reconcile gifts against bank deposit</text>
        <circle cx={26} cy={130} r={10} fill="#2E5E4E" />
        <text x={26} y={134} fontFamily="Arial" fontSize={10} fill="#F7F5F2" textAnchor="middle">3</text>
        <text x={46} y={134} fontFamily="Arial" fontSize={10} fill="#39434D">Send acknowledgment letters within 48 hours</text>
        <circle cx={26} cy={166} r={10} fill="#2E5E4E" />
        <text x={26} y={170} fontFamily="Arial" fontSize={10} fill="#F7F5F2" textAnchor="middle">4</text>
        <text x={46} y={170} fontFamily="Arial" fontSize={10} fill="#39434D">Log recurring gifts in the monthly tracker</text>
        <text x={14} y={214} fontFamily="Arial" fontSize={8} fill="#39434D" opacity={0.7}>Documented from staff interviews · owner and backup named per routine</text>
      </svg>
    ),
  },
];

export default function Process() {
  return (
    <section id="process" className="max-w-[1120px] mx-auto px-[1.4rem] py-[3.2rem] border-t border-brand-stone">
      <h2 className="font-fraunces text-[1.7rem] font-semibold text-brand-green mb-2">
        We hand over a plan, not a pitch.
      </h2>
      <p className="text-[0.97rem] max-w-[60ch] mb-7 opacity-80">
        Every project finishes with a GroundWork Plan — a practical playbook your team can use on
        day one. Here are real pages from that work.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
        {lanes.map((lane, i) => (
          <article
            key={lane.title}
            className={`bg-white rounded-[12px] border border-brand-stone p-5 shadow-sm ${
              i === lanes.length - 1 ? 'sm:col-span-2 sm:max-w-[420px]' : ''
            }`}
          >
            <h3 className="font-fraunces text-[1rem] font-semibold text-brand-green mb-0.5">
              {lane.title}
            </h3>
            <p className="text-[0.78rem] italic text-brand-slate/60 mb-3">{lane.forLine}</p>
            {lane.svg}
            <p className="text-[0.88rem] leading-snug mt-3 text-brand-slate">{lane.caption}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
