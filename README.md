# NexaSphere

> The official tech community platform for GL Bajaj Group of Institutions, Mathura.
> Built by students, for students — featuring events, activities, team management, portfolios, and more.

[![CI](https://github.com/Ayushh-Sharmaa/NexaSphere/actions/workflows/ci.yml/badge.svg)](https://github.com/Ayushh-Sharmaa/NexaSphere/actions/workflows/ci.yml)
[![Lint Markdown](https://github.com/Ayushh-Sharmaa/NexaSphere/actions/workflows/lint-markdown.yml/badge.svg)](https://github.com/Ayushh-Sharmaa/NexaSphere/actions/workflows/lint-markdown.yml)
[![License](https://img.shields.io/github/license/Ayushh-Sharmaa/NexaSphere)](LICENSE)

---

## Table of Contents

- [✨ Stack](#-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [🧪 Testing](#-testing)
- [🚢 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📚 Documentation](#-documentation)
- [📄 License](#-license)

---

## ✨ Stack

| Layer                  | Technology                                               |
| ---------------------- | -------------------------------------------------------- |
| **Website (Frontend)** | React 18 + Vite 5 + React Router v6                      |
| **Admin Dashboard**    | React 18 + Vite 5                                        |
| **Backend API**        | Node.js 20 + Express 4 (ESM)                             |
| **Database**           | PostgreSQL via Supabase (JSON file fallback for offline) |
| **Real-time**          | Socket.IO                                                |
| **Emails**             | Nodemailer / Resend / SendGrid                           |
| **Auth**               | Session-based admin auth with timing-safe comparison     |
| **Deployment**         | Frontend → Vercel · Backend → Render · Docker supported  |

---

## 📁 Project Structure

```text
NexaSphere/
├── website/              # Main public website (React + Vite)
│   ├── src/
│   │   ├── assets/       # Images, fonts, icons
│   │   ├── components/   # Reusable UI components
│   │   ├── context/      # React context providers
│   │   ├── data/         # Static data (events, activities)
│   │   ├── hooks/        # Custom React hooks
│   │   ├── pages/        # Route-level page components
│   │   ├── shared/       # Shared UI primitives (Navbar, Footer, etc.)
│   │   ├── styles/       # Global CSS + theme tokens
│   │   └── utils/        # API client, helpers, PWA utils
│   ├── .env.example      # Required environment variables
│   ├── vite.config.js
│   └── vercel.json       # Website-specific Vercel overrides
│
├── admin-dashboard/      # Admin UI (React + Vite, separate deploy)
│   ├── src/
│   ├── .env.example
│   └── vite.config.js
│
├── server/               # Express.js REST API + Socket.IO
│   ├── config/           # DB, socket, and service config
│   ├── controllers/      # Route handler functions
│   ├── middleware/        # Auth, rate limiting, error handling
│   ├── migrations/        # Database migration files
│   ├── repositories/     # DB access layer (repository pattern)
│   ├── routes/           # Express route definitions
│   ├── services/         # Business logic
│   ├── utils/            # Helpers (Sentry, email, etc.)
│   ├── validators/       # Zod schema validators
│   ├── index.js          # Entry point
│   ├── .env.example      # All required environment variables
│   └── Dockerfile        # Production Docker image
│
├── server-python/        # FastAPI ML/AI microservice (optional)
├── server-java/          # Spring Boot alternative (experimental)
├── google-apps-script/   # Google Sheets / Forms integration scripts
├── docs/                 # Deep-dive documentation
├── e2e/                  # Playwright end-to-end tests
│
├── vercel.json           # Root Vercel config (deploys website/)
├── render.yaml           # Render config (deploys server/)
├── docker-compose.yml    # Local dev with Docker
├── package.json          # Monorepo root (npm workspaces)
└── .github/workflows/    # CI/CD GitHub Actions
```

---

## 🚀 Quick Start

> **3 steps to get NexaSphere running locally.**

### 1. Clone & Install

```bash
git clone https://github.com/Ayushh-Sharmaa/NexaSphere.git
cd NexaSphere
npm install
```

### 2. Configure Environment

```bash
cp website/.env.example website/.env.local
cp admin-dashboard/.env.example admin-dashboard/.env.local
cp server/.env.example server/.env
```

Minimum values needed in `server/.env`:

```env
PORT=8787
NODE_ENV=development
CORS_ORIGIN=http://localhost:5175,http://localhost:5001
ADMIN_USERNAME=your-admin
ADMIN_PASSWORD=YourPass123!
ADMIN_EVENT_PASSWORD=EventPass456!
```

### 3. Run Development Servers

```bash
npm run dev:all     # Start website + admin + API together
```

Or start services individually:

| Command                 | Service          | URL                          |
| ----------------------- | ---------------- | ---------------------------- |
| `npm run dev:website`   | Website          | http://localhost:5175        |
| `npm run dev:admin`     | Admin Dashboard  | http://localhost:5001        |
| `npm run dev:server`    | Backend API      | http://localhost:8787        |
| —                       | API Health Check | http://localhost:8787/health |

> **Tip:** The website works in **offline mode** when `VITE_API_BASE` is empty.
> All data comes from localStorage / static JSON files — no backend needed.

---

## 🧪 Testing

```bash
npm test                # Website unit tests (Vitest)
npm run test:server     # Server unit tests (Node test runner)
npx playwright test     # End-to-end tests (Playwright)
```

---

## 🚢 Deployment

| Target              | Config File       | Notes                                              |
| ------------------- | ----------------- | -------------------------------------------------- |
| Vercel (frontend)   | `vercel.json`     | Connect repo, set `VITE_API_BASE` env var          |
| Render (backend)    | `render.yaml`     | Set `sync: false` env vars in Render dashboard     |
| Docker (backend)    | `server/Dockerfile` | `docker build -t nexasphere-api ./server`        |
| Docker Compose      | `docker-compose.yml` | `docker-compose up --build`                     |

For full deployment instructions see [docs/deployment.md](docs/deployment.md).

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

This project is part of **GSSoC 2026** — check the open issues for tasks labelled `good first issue`.

---

## 📚 Documentation

Deep-dive references live in the [`/docs`](docs/) directory:

| Document                                            | Description                              |
| --------------------------------------------------- | ---------------------------------------- |
| [docs/architecture.md](docs/architecture.md)        | System architecture & component overview |
| [docs/api-reference.md](docs/api-reference.md)      | REST API endpoint reference              |
| [docs/deployment.md](docs/deployment.md)            | Full deployment guide (Vercel / Render / Docker) |
| [docs/database-backups.md](docs/database-backups.md) | Database backup & restore procedures    |
| [docs/DATABASE_MIGRATIONS.md](docs/DATABASE_MIGRATIONS.md) | Running & writing DB migrations   |

---

## 📄 License

[MIT](LICENSE) © NexaSphere Core Team
