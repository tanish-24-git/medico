'use client';

import Link from 'next/link';
import { Heart } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-4">
          <div>
            <div className="flex items-center gap-2 pb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                <Heart className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-semibold text-foreground">MedicoChatbot</span>
            </div>
            <p className="text-sm text-foreground/60">Healthcare should be understandable for everyone.</p>
          </div>

          <div>
            <h4 className="font-semibold text-foreground">Product</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <Link href="/chat" className="text-sm text-foreground/60 transition-colors hover:text-foreground">
                  Chat
                </Link>
              </li>
              <li>
                <Link href="/reports" className="text-sm text-foreground/60 transition-colors hover:text-foreground">
                  Reports
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground">Legal</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <Link href="#" className="text-sm text-foreground/60 transition-colors hover:text-foreground">
                  Privacy
                </Link>
              </li>
              <li>
                <Link href="#" className="text-sm text-foreground/60 transition-colors hover:text-foreground">
                  Terms
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground">Contact</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <Link href="#" className="text-sm text-foreground/60 transition-colors hover:text-foreground">
                  hello@medicochatbot.com
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 border-t border-border pt-8">
          <p className="text-center text-sm text-foreground/60">
            Built with AI + Care <Heart className="inline h-4 w-4 text-red-500" />
          </p>
        </div>
      </div>
    </footer>
  );
}
