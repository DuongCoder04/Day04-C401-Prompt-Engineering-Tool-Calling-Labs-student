import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/* ── Mock data ── */
const CARDS = [
  {
    title: 'Research Agent',
    subtitle: 'Modular AI toolkit — 4 tools, eval-driven, extensible',
    gradient: 'from-zinc-900 to-zinc-700',
  },
  {
    title: 'Calculate',
    subtitle: 'Safe expression evaluator — sin, cos, sqrt, log, π',
    gradient: 'from-amber-600 to-orange-700',
  },
  {
    title: 'Web Search',
    subtitle: 'DuckDuckGo instant answers — no API key required',
    gradient: 'from-sky-600 to-blue-700',
  },
  {
    title: 'Music Search',
    subtitle: 'iTunes Search API — find songs, albums, artists',
    gradient: 'from-violet-600 to-purple-700',
  },
  {
    title: 'Story Search',
    subtitle: 'Open Library — discover books by title or author',
    gradient: 'from-emerald-600 to-teal-700',
  },
];

const FLUID_EASE: [number, number, number, number] = [0.16, 1, 0.3, 1];
const N = CARDS.length;

interface Props {
  interval?: number;
  spread?: number;
  startScale?: number;
}

export default function StackedCardCarousel({
  interval = 4000,
  spread = 20,
  startScale = 0.7,
}: Props) {
  const [active, setActive] = useState(0);

  /* ── Auto-loop ── */
  useEffect(() => {
    const id = setInterval(() => setActive((a) => (a + 1) % N), interval);
    return () => clearInterval(id);
  }, [interval]);

  return (
    <div className="relative" style={{ overflow: 'hidden', height: '420px' }}>
      {CARDS.map((card, i) => {
        /* 0 = front, N-1 = deepest */
        const pos = (i - active + N) % N;

        const y = pos * spread;
        const scale = 1 - pos * ((1 - startScale) / (N - 1));

        const isFront = pos === 0;
        const zIndex = 100 - pos;

        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: 0,
              zIndex,
              height: '100%',
            }}
          >
            <motion.div
              style={{
                width: '100%',
                maxWidth: '28rem',
                margin: '0 auto',
                transformOrigin: 'center center',
                willChange: 'transform, opacity',
              }}
              animate={{ y, scale, opacity: 1 - pos * (1 / (N - 1 + 0.5)) }}
              transition={{ duration: 0.55, ease: FLUID_EASE }}
            >
              <div
                className={`rounded-2xl bg-gradient-to-br ${card.gradient} p-6 text-white`}
                style={{
                  boxShadow: isFront
                    ? '0 25px 50px -12px rgba(0,0,0,0.25)'
                    : '0 8px 30px -8px rgba(0,0,0,0.15)',
                }}
              >
                {/* Placeholder image area */}
                <div className="mb-4 flex h-36 items-center justify-center rounded-xl bg-white/10">
                  <svg
                    className="h-10 w-10 text-white/40"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.41a2.25 2.25 0 013.182 0l2.909 2.91m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
                    />
                  </svg>
                </div>

                <h3 className="text-lg font-semibold tracking-tight">
                  {card.title}
                </h3>
                <p className="mt-1 text-sm text-white/70">{card.subtitle}</p>
              </div>
            </motion.div>
          </div>
        );
      })}

      {/* Dots navigation */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          gap: '8px',
        }}
      >
        {CARDS.map((_, i) => (
          <button
            key={i}
            onClick={() => setActive(i)}
            style={{
              height: '8px',
              borderRadius: '9999px',
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.5s',
              width: i === active ? '24px' : '8px',
              backgroundColor: i === active ? '#18181b' : '#d4d4d8',
            }}
            aria-label={`Go to card ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
