const lanes = [
  {
    num: '01',
    title: 'Executive GroundWork',
    body: 'Hiring an experienced leader is tough with a volunteer board and stretched staff. While you search, we gather the research, plans, and institutional knowledge so whoever steps in can lead from day one.',
  },
  {
    num: '02',
    title: 'Development GroundWork',
    body: 'We audit your CRM, fix the easy stuff, and document what needs attention. We research major donors and review past fundraising events — so your next hire inherits a head start, not a mess.',
  },
  {
    num: '03',
    title: 'Program GroundWork',
    body: 'We consolidate all grant deadlines into one place, collect feedback from program participants, and reach out to partner organizations to let them know help is on the way.',
  },
  {
    num: '04',
    title: 'Communications GroundWork',
    body: 'A brand voice guide and ready-to-post, pre-approved content. Your new hire publishes in week one, not month three.',
  },
  {
    num: '05',
    title: 'Operations GroundWork',
    body: 'A systems audit with step-by-step procedures documented from the people who do the work — so nothing lives in someone\'s head anymore.',
  },
];

export default function Lanes() {
  return (
    <section className="max-w-[1120px] mx-auto px-[1.4rem] py-[3.2rem] border-t border-brand-stone">
      <h2 className="font-fraunces text-[1.7rem] font-semibold text-brand-green mb-6">
        Our services
      </h2>
      <div className="space-y-0 divide-y divide-brand-stone border-t border-brand-stone">
        {lanes.map((lane) => (
          <div key={lane.title} className="flex gap-6 py-5">
            <span className="font-fraunces text-[1.4rem] text-brand-stone/60 font-semibold shrink-0 w-8 pt-0.5">
              {lane.num}
            </span>
            <div>
              <h3 className="font-fraunces text-[1.05rem] font-semibold text-brand-green mb-1">
                {lane.title}
              </h3>
              <p className="text-[0.93rem] leading-relaxed max-w-[56ch]">{lane.body}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
