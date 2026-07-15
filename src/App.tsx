import Header from './components/Header';
import Hero from './components/Hero';
import Process from './components/Process';
import Lanes from './components/Lanes';
import Promise from './components/Promise';
import Pricing from './components/Pricing';
import Bio from './components/Bio';
import ContactForm from './components/ContactForm';
import Footer from './components/Footer';

export default function App() {
  return (
    <div className="bg-brand-bg min-h-screen">
      <Header />
      <Hero />
      <div className="bg-white/60"><Process /></div>
      <Lanes />
      <div className="bg-white/60"><Promise /></div>
      <Pricing />
      <div className="bg-white/60"><Bio /></div>
      <ContactForm />
      <Footer />
    </div>
  );
}
