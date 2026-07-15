export default function Footer() {
  return (
    <footer className="max-w-[1120px] mx-auto px-[1.4rem] py-10 border-t border-brand-stone text-[0.9rem]">
      <p>
        <strong>Mission GroundWork</strong> · A project of MG Digital LLC ·{' '}
        <a
          href="mailto:mozartguerrier@gmail.com"
          className="text-brand-green underline underline-offset-2 hover:text-brand-green-dark transition-colors"
        >
          mozartguerrier@gmail.com
        </a>
      </p>
      <p className="text-[0.85rem] opacity-80 mt-3">
        We are not a search firm, and we never place or recommend candidates. The hire is yours; the
        ground is ours. We are not fractional/interim, and we don't offer marketing retainers.
      </p>
      <p className="text-[0.85rem] opacity-80 mt-2">© 2026 MG Digital LLC</p>
    </footer>
  );
}
