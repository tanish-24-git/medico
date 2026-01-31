'use client';

import { Navbar } from '@/components/navbar';
import { Footer } from '@/components/footer';
import { ReportCard } from '@/components/report-card';
import { Button } from '@/components/ui/button';
import { Upload, Loader2, FileText } from 'lucide-react';
import { useState, useEffect } from 'react';
import { apiRequest, API_ENDPOINTS } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface Metric {
  label: string;
  value: string;
  status: 'normal' | 'warning' | 'alert';
}

interface Report {
  id: number;
  filename: string;
  created_at: string;
  processing_status: string;
  parsed_metrics?: Record<string, any>;
  ai_summary?: string;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setIsLoading(true);
      const data = await apiRequest<{ reports: Report[] }>(API_ENDPOINTS.REPORTS.LIST);
      setReports(data.reports);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch medical reports.',
        variant: 'destructive',
      });
      console.error('Fetch reports error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatMetrics = (metrics?: Record<string, any>): Metric[] => {
    if (!metrics) return [];
    return Object.entries(metrics).map(([key, value]) => ({
      label: key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
      value: String(value),
      status: 'normal' as const, // Future: Backend could provide status
    }));
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Navbar />

      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="mb-12">
            <h1 className="text-4xl font-bold tracking-tight text-foreground">
              Your Medical Reports
            </h1>
            <p className="mt-2 text-lg text-foreground/70">
              Upload and manage your health reports. Get instant explanations and insights.
            </p>
          </div>

          <div className="mb-12 flex gap-4">
            <Button size="lg" className="gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
              <Upload className="h-5 w-5" />
              Upload New Report
            </Button>
            <Button variant="outline" size="lg" onClick={fetchReports} disabled={isLoading}>
              {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : 'Refresh'}
            </Button>
          </div>

          <div className="mb-8">
            <h2 className="mb-6 text-2xl font-bold text-foreground">Recent Reports</h2>
            
            {isLoading ? (
              <div className="flex h-64 items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : reports.length > 0 ? (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {reports.map((report) => (
                  <ReportCard 
                    key={report.id} 
                    title={report.filename}
                    date={formatDate(report.created_at)}
                    metrics={formatMetrics(report.parsed_metrics)}
                  />
                ))}
              </div>
            ) : (
              <div className="flex h-64 flex-col items-center justify-center rounded-lg border-2 border-dashed border-muted p-12 text-center">
                <div className="mb-4 rounded-full bg-muted p-3">
                  <FileText className="h-8 w-8 text-muted-foreground" />
                </div>
                <h3 className="text-lg font-medium text-foreground">No reports found</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Upload your first medical report to see it here.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
