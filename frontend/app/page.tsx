import { Navbar } from '@/components/navbar';
import { Footer } from '@/components/footer';
import { HeroSection } from '@/components/hero-section';
import { WorkflowTimeline } from '@/components/workflow-timeline';
import { FeaturesSection } from '@/components/features-section';
import { TestimonialsSection } from '@/components/testimonials-section';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <HeroSection />
      <WorkflowTimeline />
      <FeaturesSection />
      <TestimonialsSection />
      <Footer />
    </div>
  );
}
