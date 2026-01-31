'use client';

import { Star } from 'lucide-react';

const testimonials = [
  {
    quote: 'My blood test finally made sense.',
    author: 'Sarah Johnson',
    role: 'Patient',
  },
  {
    quote: 'Feels like chatting with a friendly doctor.',
    author: 'Michael Chen',
    role: 'Healthcare Advocate',
  },
  {
    quote: 'Best healthcare AI tool ever.',
    author: 'Emma Rodriguez',
    role: 'Patient',
  },
];

export function TestimonialsSection() {
  return (
    <section className="border-b border-border bg-background py-20 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Loved by Patients
          </h2>
          <p className="mt-4 text-lg text-foreground/70">
            Join thousands of people taking control of their health
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="animate-fade-in-up rounded-xl border border-border bg-card p-8 shadow-sm transition-all hover:shadow-md"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="mb-4 flex gap-1">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 fill-primary text-primary" />
                ))}
              </div>
              <p className="mb-6 text-lg italic text-foreground">"{testimonial.quote}"</p>
              <div>
                <p className="font-semibold text-foreground">{testimonial.author}</p>
                <p className="text-sm text-foreground/60">{testimonial.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
