export default function Promise() {
  return (
    <section className="max-w-[1120px] mx-auto px-[1.4rem] py-[3.2rem] border-t border-brand-stone">
      <h2 className="font-fraunces text-[1.7rem] font-semibold text-brand-green mb-6">
        Our promise
      </h2>
      <div className="space-y-6 max-w-[600px]">
        <div className="flex gap-4 items-start">
          <div className="w-1 self-stretch rounded-full bg-brand-green shrink-0" />
          <div>
            <h3 className="font-fraunces font-semibold text-brand-green text-[1rem] mb-1">Mission-focused</h3>
            <p className="text-[0.93rem]">We work exclusively in the nonprofit sector. The stakes, the constraints, and the culture are ones we understand — and take seriously.</p>
          </div>
        </div>
        <div className="flex gap-4 items-start">
          <div className="w-1 self-stretch rounded-full bg-brand-clay shrink-0" />
          <div>
            <h3 className="font-fraunces font-semibold text-brand-green text-[1rem] mb-1">Reasonable</h3>
            <p className="text-[0.93rem]">Flat scope. Clear deliverables. You know what you're getting before we start — and we don't pad the work to justify the price.</p>
          </div>
        </div>
        <div className="flex gap-4 items-start">
          <div className="w-1 self-stretch rounded-full bg-brand-stone shrink-0" />
          <div>
            <h3 className="font-fraunces font-semibold text-brand-green text-[1rem] mb-1">Specific</h3>
            <p className="text-[0.93rem]">We do one thing: get a new hire ready to work. No retainers, no sprawl, no generalist advice. Just the groundwork.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
