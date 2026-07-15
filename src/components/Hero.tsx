import { useState } from 'react';

const deliverables = [
  'grant calendars',
  'stakeholder maps',
  'content calendars',
  'SOPs',
  'program baselines',
];

const roles = [
  'Executive Director',
  'Development Director',
  'Program Leader',
  'Communications Manager',
  'Operations Manager',
];

export default function Hero() {
  const [idx, setIdx] = useState(0);

  return (
    <section className="max-w-[1120px] mx-auto px-[1.4rem] py-12">
      <h1 className="font-fraunces text-[clamp(2rem,5vw,3.1rem)] leading-[1.15] font-semibold text-brand-green max-w-[17ch]">
        Helping your team start on solid ground.
      </h1>

      <div className="mt-8 max-w-[62ch] space-y-4">
        <p className="text-[1.1rem] leading-relaxed">
          You apply for an urgent program or role for your team. It takes months to get the funds —
          and then it's time to interview and rebuild programs. Again.
        </p>
        <p className="text-[1.1rem] leading-relaxed">
          You needed to get started months ago. Too many people — from executive directors to
          caseworkers — are overwhelmed.
        </p>
        <p className="text-[1.05rem] leading-relaxed">
          GroundWork does the pre-work before a new hire gets on board so they hit the ground
          running. From{' '}
          <a
            href="#process"
            onClick={() => setIdx((idx + 1) % deliverables.length)}
            className="font-semibold text-brand-green underline underline-offset-4 decoration-brand-clay cursor-pointer transition-colors hover:text-brand-clay focus:outline-none"
          >
            {deliverables[idx]}
          </a>{' '}
          to helping a new executive director run better board meetings — we provide action plans
          for five roles:
        </p>

        <ul className="space-y-1 pl-1">
          {roles.map((role) => (
            <li key={role} className="flex items-center gap-2.5 text-[0.97rem]">
              <span className="w-1.5 h-1.5 rounded-full bg-brand-clay shrink-0" />
              {role}
            </li>
          ))}
        </ul>

        <p className="text-[1rem] font-medium text-brand-slate border-l-[3px] border-brand-clay pl-4">
          We aren't selling theories. We help you build an action plan and get out of the way.
        </p>
      </div>

      <a
        href="#process"
        className="inline-block mt-7 bg-brand-green text-white no-underline px-[1.7rem] py-[0.9rem] rounded-lg font-semibold text-base transition-colors duration-200 hover:bg-brand-green-dark focus:outline-none focus:ring-[3px] focus:ring-brand-clay focus:ring-offset-2"
      >
        See the plans
      </a>
    </section>
  );
}
