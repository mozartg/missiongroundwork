import { useState, FormEvent } from 'react';
import { CheckCircle, AlertCircle } from 'lucide-react';

type Status = 'idle' | 'submitting' | 'success' | 'error';

export default function ContactForm() {
  const [status, setStatus] = useState<Status>('idle');

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('submitting');

    const form = e.currentTarget;
    const data = new FormData(form);

    try {
      const res = await fetch('https://formspree.io/f/xrenbylz', {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' },
      });

      if (res.ok) {
        setStatus('success');
        form.reset();
      } else {
        setStatus('error');
      }
    } catch {
      setStatus('error');
    }
  }

  const inputClass =
    'w-full px-3 py-2.5 border border-brand-stone rounded-md font-inter text-[0.95rem] bg-white transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-brand-green focus:border-brand-green';
  const labelClass = 'text-[0.85rem] font-medium block mb-1';

  return (
    <section id="contact" className="max-w-[1120px] mx-auto px-[1.4rem] py-[3.2rem] border-t border-brand-stone">
      <h2 className="font-fraunces text-[1.7rem] font-semibold text-brand-green mb-2">
        Let's talk about working together.
      </h2>
      <p className="max-w-[56ch] mb-6">
        Fill in the form and I'll reach out within 24 hours — just a conversation to see if we're
        a fit.
      </p>

      {status === 'success' ? (
        <div className="flex items-start gap-3 bg-white border border-brand-stone rounded-xl p-6 max-w-[520px]">
          <CheckCircle size={22} className="text-brand-green mt-0.5 shrink-0" />
          <div>
            <p className="font-semibold text-brand-green">Message sent!</p>
            <p className="text-[0.9rem] mt-1">
              Thanks for reaching out. I'll be in touch within 24 hours.
            </p>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="max-w-[520px] space-y-4">
          <div>
            <label htmlFor="name" className={labelClass}>
              Your name
            </label>
            <input type="text" id="name" name="name" required className={inputClass} />
          </div>

          <div>
            <label htmlFor="email" className={labelClass}>
              Email address
            </label>
            <input type="email" id="email" name="_replyto" required className={inputClass} />
          </div>

          <div>
            <label htmlFor="org" className={labelClass}>
              Organization
            </label>
            <input type="text" id="org" name="organization" className={inputClass} />
          </div>

          <div>
            <label htmlFor="message" className={labelClass}>
              What role are you looking to ground?
            </label>
            <textarea
              id="message"
              name="message"
              required
              rows={4}
              placeholder="e.g., Development Director, Executive Director, Operations Manager..."
              className={`${inputClass} resize-y`}
            />
          </div>

          {status === 'error' && (
            <div className="flex items-center gap-2 text-[0.9rem] text-red-600">
              <AlertCircle size={16} />
              Something went wrong. Please try again or email me directly.
            </div>
          )}

          <div className="flex items-center gap-4 flex-wrap pt-1">
            <button
              type="submit"
              disabled={status === 'submitting'}
              className="bg-brand-green text-white px-[1.7rem] py-[0.9rem] rounded-lg font-semibold text-base transition-colors duration-200 hover:bg-brand-green-dark focus:outline-none focus:ring-[3px] focus:ring-brand-clay focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {status === 'submitting' ? 'Sending...' : 'Send inquiry'}
            </button>
            <span className="text-[0.85rem] opacity-70">
              or email me directly at{' '}
              <a
                href="mailto:mozartguerrier@gmail.com"
                className="text-brand-green underline underline-offset-2"
              >
                mozartguerrier@gmail.com
              </a>
            </span>
          </div>

          {/* Anti-spam honeypot */}
          <input type="text" name="_gotcha" className="hidden" />
        </form>
      )}

      <p className="text-[0.85rem] opacity-80 mt-4">
        * Your data stays private. I only use it to respond to your inquiry.
      </p>
    </section>
  );
}
