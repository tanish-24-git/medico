'use client';

import { FileText, MessageCircle, Brain, Lock, BarChart3, Zap } from 'lucide-react';

const features = [
  {
    icon: FileText,
    title: 'Report Upload & Explanation',
    description: 'Upload blood reports, X-rays, and lab results. Get instant, clear explanations.',
  },
  {
    icon: MessageCircle,
    title: 'Real-Time Medical Chat',
    description: 'Ask follow-up questions and get personalized answers instantly.',
  },
  {
    icon: Brain,
    title: 'Layman-Friendly Health Insights',
    description: 'Complex medical terms translated into language anyone can understand.',
  },
  {
    icon: Lock,
    title: 'Secure Google Login',
    description: 'Your health data is private, encrypted, and protected.',
  },
  {
    icon: BarChart3,
    title: 'AI Monitoring with LangSmith',
    description: 'Track your health journey with intelligent analytics.',
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Get answers in seconds, not hours. Powered by advanced AI.',
  },
];

export function FeaturesSection() {
  return (
    <section className="border-b border-border bg-background py-20 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Powerful Features
          </h2>
          <p className="mt-4 text-lg text-foreground/70">
            Everything you need for better health understanding
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="animate-fade-in-up group rounded-xl border border-border bg-card p-6 transition-all hover:border-primary/50 hover:shadow-lg"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3 text-primary transition-colors group-hover:bg-primary/20">
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold text-foreground">
                  {feature.title}
                </h3>
                <p className="text-foreground/60">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
