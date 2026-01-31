'use client';

import { Upload, Zap, BookOpen, MessageSquare, Activity } from 'lucide-react';

const steps = [
  {
    icon: Upload,
    title: 'Upload Report',
    description: 'Share your medical documents securely',
  },
  {
    icon: Zap,
    title: 'AI Reads Values',
    description: 'Advanced analysis in seconds',
  },
  {
    icon: BookOpen,
    title: 'Simple Language',
    description: 'Complex terms explained clearly',
  },
  {
    icon: MessageSquare,
    title: 'Chat Naturally',
    description: 'Ask questions like a friend',
  },
  {
    icon: Activity,
    title: 'Health Guidance',
    description: 'Personalized insights and tips',
  },
];

export function WorkflowTimeline() {
  return (
    <section className="border-b border-border bg-background py-20 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            How It Works
          </h2>
          <p className="mt-4 text-lg text-foreground/70">
            Five simple steps to understand your health better
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-5">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="relative">
                <div className="flex flex-col items-center">
                  <div className="relative mb-6">
                    <div className="absolute inset-0 rounded-full bg-primary/10 blur" />
                    <div className="relative flex h-16 w-16 items-center justify-center rounded-full border-2 border-primary bg-card">
                      <Icon className="h-8 w-8 text-primary" />
                    </div>
                  </div>

                  <h3 className="text-center text-lg font-semibold text-foreground">
                    {step.title}
                  </h3>
                  <p className="mt-2 text-center text-sm text-foreground/60">
                    {step.description}
                  </p>
                </div>

                {index < steps.length - 1 && (
                  <div className="absolute -right-4 top-8 hidden h-0.5 w-8 bg-gradient-to-r from-primary/50 to-transparent lg:block" />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
