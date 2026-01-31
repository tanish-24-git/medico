'use client';

import { Button } from '@/components/ui/button';
import { FileText, ChevronRight } from 'lucide-react';

interface ReportCardProps {
  title: string;
  metrics: {
    label: string;
    value: string;
    status?: 'normal' | 'warning' | 'alert';
  }[];
  date: string;
}

const statusColors = {
  normal: 'text-green-600',
  warning: 'text-yellow-600',
  alert: 'text-red-600',
};

export function ReportCard({ title, metrics, date }: ReportCardProps) {
  return (
    <div className="animate-fade-in-up rounded-xl border border-border bg-card p-6 transition-all hover:shadow-lg">
      <div className="mb-4 flex items-start justify-between">
        <div className="flex items-start gap-3">
          <div className="rounded-lg bg-primary/10 p-2">
            <FileText className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h3 className="font-semibold text-foreground">{title}</h3>
            <p className="text-sm text-foreground/60">{date}</p>
          </div>
        </div>
      </div>

      <div className="mb-6 space-y-3">
        {metrics.map((metric, index) => (
          <div key={index} className="flex items-center justify-between">
            <span className="text-sm text-foreground/70">{metric.label}</span>
            <span
              className={`font-semibold ${statusColors[metric.status || 'normal']}`}
            >
              {metric.value}
            </span>
          </div>
        ))}
      </div>

      <Button className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
        Explain This Report
        <ChevronRight className="h-4 w-4" />
      </Button>
    </div>
  );
}
