'use client';

import { Navbar } from '@/components/navbar';
import { Footer } from '@/components/footer';
import { Heart, Shield, Zap, Users } from 'lucide-react';

const values = [
  {
    icon: Heart,
    title: 'Patient-Centric',
    description: 'We design everything with patients in mind, prioritizing clarity and ease of use.',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'Your health data is sacred. We use enterprise-grade encryption and never sell your information.',
  },
  {
    icon: Zap,
    title: 'Innovative',
    description: 'Cutting-edge AI technology that understands healthcare and delivers accurate insights.',
  },
  {
    icon: Users,
    title: 'Accessible',
    description: 'Healthcare information should be free and accessible to everyone, everywhere.',
  },
];

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Navbar />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="border-b border-border py-20 sm:py-32">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
                Healthcare should be understandable for everyone.
              </h1>
              <p className="mt-6 text-lg text-foreground/70">
                MedicoChatbot bridges the gap between patients and complex medical reports. We believe
                everyone deserves to understand their own health.
              </p>
            </div>
          </div>
        </section>

        {/* Mission Section */}
        <section className="border-b border-border py-20 sm:py-32">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid gap-12 lg:grid-cols-2">
              <div>
                <h2 className="text-3xl font-bold text-foreground">Our Mission</h2>
                <p className="mt-4 text-lg text-foreground/70">
                  We're on a mission to democratize healthcare understanding. Too many people receive their
                  medical reports and feel confused or worried. Our AI assistant explains complex medical
                  information in simple, friendly language.
                </p>
                <p className="mt-4 text-lg text-foreground/70">
                  Built with AI, privacy, and trust at our core, MedicoChatbot is here to empower you to
                  take control of your health journey.
                </p>
              </div>
              <div className="rounded-xl border border-border bg-card p-8">
                <h3 className="text-xl font-semibold text-foreground">By the Numbers</h3>
                <div className="mt-8 space-y-6">
                  <div>
                    <p className="text-4xl font-bold text-primary">50K+</p>
                    <p className="text-foreground/60">Reports Analyzed</p>
                  </div>
                  <div>
                    <p className="text-4xl font-bold text-primary">10K+</p>
                    <p className="text-foreground/60">Happy Patients</p>
                  </div>
                  <div>
                    <p className="text-4xl font-bold text-primary">99.9%</p>
                    <p className="text-foreground/60">Uptime</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Values Section */}
        <section className="border-b border-border py-20 sm:py-32">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <h2 className="mb-12 text-center text-3xl font-bold text-foreground">Our Values</h2>
            <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
              {values.map((value, index) => {
                const Icon = value.icon;
                return (
                  <div key={index} className="rounded-xl border border-border bg-card p-6">
                    <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3 text-primary">
                      <Icon className="h-6 w-6" />
                    </div>
                    <h3 className="mb-2 font-semibold text-foreground">{value.title}</h3>
                    <p className="text-sm text-foreground/60">{value.description}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="border-b border-border py-20 sm:py-32">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <h2 className="mb-12 text-center text-3xl font-bold text-foreground">
              Designed for patients. Powered by intelligence.
            </h2>
            <div className="text-center">
              <p className="text-lg text-foreground/70">
                Our team combines expertise in healthcare, AI, and design to create a platform that truly
                serves patients. We're passionate about making healthcare accessible to everyone.
              </p>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="py-20 sm:py-32">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="rounded-xl border border-border bg-card p-12 text-center">
              <h2 className="text-3xl font-bold text-foreground">Have Questions?</h2>
              <p className="mt-4 text-lg text-foreground/70">
                We'd love to hear from you. Get in touch with our team.
              </p>
              <a
                href="mailto:hello@medicochatbot.com"
                className="mt-8 inline-block rounded-lg bg-primary px-6 py-3 font-semibold text-primary-foreground transition-colors hover:bg-primary/90"
              >
                Contact Us
              </a>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
