# Tech Stack Detection Patterns

Reference guide for identifying technology stacks in different projects.

---

## Dependency Files by Language

### JavaScript / TypeScript

| File | Package Manager | Description |
|------|---------------|-------------|
| `package.json` | npm/yarn/pnpm | Main dependency manifest |
| `package-lock.json` | npm | Lock file for npm |
| `yarn.lock` | yarn | Lock file for Yarn |
| `pnpm-lock.yaml` | pnpm | Lock file for pnpm |

**Common frameworks detection:**
- `react` → React.js
- `next` → Next.js
- `nuxt` → Nuxt.js
- `vue` → Vue.js
- `@angular/*` → Angular
- `svelte` → Svelte
- `gatsby` → Gatsby
- `express` → Express.js
- `@nestjs/*` → NestJS
- `astro` → Astro

### Python

| File | Package Manager | Description |
|------|---------------|-------------|
| `requirements.txt` | pip | Simple requirements file |
| `setup.py` | setuptools | Legacy setup script |
| `pyproject.toml` | PEP 518 | Modern Python packaging |
| `Pipfile` | pipenv | Pipenv lock file |
| `poetry.lock` | poetry | Poetry lock file |

**Common frameworks detection:**
- `django` → Django
- `flask` → Flask
- `fastapi` → FastAPI
- `tornado` → Tornado
- `aiohttp` → AIOHTTP
- `celery` → Celery (task queue)
- `sqlalchemy` → SQLAlchemy (ORM)

### Go

| File | Package Manager | Description |
|------|---------------|-------------|
| `go.mod` | Go Modules | Module definition |
| `go.sum` | Go Modules | Dependency checksums |

**Common frameworks detection:**
- `github.com/gin-gonic/gin` → Gin
- `github.com/labstack/echo` → Echo
- `github.com/gofiber/fiber` → Fiber
- `github.com/gorilla/*` → Gorilla Toolkit

### Rust

| File | Package Manager | Description |
|------|---------------|-------------|
| `Cargo.toml` | Cargo | Package manifest |
| `Cargo.lock` | Cargo | Lock file |

**Common frameworks detection:**
- `actix-web` → Actix Web
- `rocket` → Rocket
- `tokio` → Tokio (async runtime)

### Java / Kotlin

| File | Build Tool | Description |
|------|-----------|-------------|
| `pom.xml` | Maven | Maven POM file |
| `build.gradle` | Gradle | Gradle build file |
| `build.gradle.kts` | Gradle | Gradle Kotlin DSL |

**Common frameworks detection:**
- `org.springframework.boot` → Spring Boot
- `org.springframework.*` → Spring Framework
- `org.hibernate` → Hibernate (ORM)
- `junit` → JUnit (testing)

### Ruby

| File | Package Manager | Description |
|------|---------------|-------------|
| `Gemfile` | Bundler | Ruby gems manifest |
| `Gemfile.lock` | Bundler | Lock file |

**Common frameworks detection:**
- `rails` → Ruby on Rails
- `sinatra` → Sinatra

### PHP

| File | Package Manager | Description |
|------|---------------|-------------|
| `composer.json` | Composer | PHP packages manifest |

**Common frameworks detection:**
- `laravel/*` → Laravel
- `symfony/*` → Symfony
- `wordpress` → WordPress

---

## Build Tools Detection

### JavaScript Ecosystem

| Tool | Detection Pattern | Description |
|------|-----------------|-------------|
| Webpack | `webpack`, `webpack-cli` | Module bundler |
| Vite | `vite` | Next-gen build tool |
| Rollup | `rollup` | Module bundler |
| esbuild | `esbuild` | Fast bundler |
| Parcel | `parcel` | Zero-config bundler |
| Turbopack | `turbo` | Rust-based bundler |
| Gulp | `gulp` | Task runner |
| Grunt | `grunt` | Task runner |
| Babel | `@babel/core`, `babel-core` | JavaScript transpiler |
| TypeScript | `typescript` | TypeScript compiler |

### Testing Tools

| Tool | Detection Pattern | Language |
|------|-----------------|----------|
| Jest | `jest` | JS/TS |
| Vitest | `vitest` | JS/TS |
| Mocha | `mocha` | JS/TS |
| Cypress | `cypress` | E2E testing |
| Playwright | `@playwright/test` | E2E testing |
| Pytest | `pytest` | Python |
| JUnit | `junit` | Java |
| RSpec | `rspec` | Ruby |

---

## Configuration Files

### TypeScript / JavaScript
- `tsconfig.json` → TypeScript configuration
- `jsconfig.json` → JavaScript configuration
- `.eslintrc.*` → ESLint configuration
- `.prettierrc.*` → Prettier configuration

### Python
- `pytest.ini` → Pytest configuration
- `tox.ini` → Tox configuration
- `.flake8` → Flake8 configuration

### Go
- `go.mod` → Go modules configuration

### Docker
- `Dockerfile` → Docker image build
- `docker-compose.yml` → Docker Compose

### CI/CD
- `.github/workflows/*.yml` → GitHub Actions
- `.gitlab-ci.yml` → GitLab CI
- `.travis.yml` → Travis CI
- `circleci` → CircleCI

---

## Entry Point Patterns

### Python
- `main.py` → Main entry point
- `app.py` → Application entry (Flask/Django)
- `run.py` → Run script
- `server.py` → Server script
- `wsgi.py` → WSGI entry point

### JavaScript / TypeScript
- `index.js` / `index.ts` → Default entry
- `main.js` / `main.ts` → Main entry
- `server.js` / `server.ts` → Server entry
- `app.js` / `app.ts` → Application entry

### React
- `src/index.js` / `src/index.tsx` → React entry
- `src/main.jsx` / `src/main.tsx` → React with Vite

### Vue
- `src/main.js` / `src/main.ts` → Vue entry

### Next.js
- `pages/index.js` / `pages/index.tsx` → Pages router
- `app/page.js` / `app/page.tsx` → App router

### Nuxt
- `pages/index.vue` → Page entry

### Go
- `main.go` → Main entry
- `cmd/*/main.go` → Multi-module entry

### Rust
- `main.rs` / `src/main.rs` → Main entry

### Java
- `src/main/java/*/Main.java` → Main class
- `src/main/java/*/Application.java` → Spring Boot application

---

## Framework-Specific Directory Patterns

### React
```
src/
├── components/     # React components
├── pages/          # Page components
├── hooks/          # Custom hooks
├── context/        # Context providers
├── utils/          # Utility functions
└── App.jsx/tsx     # Root component
```

### Vue
```
src/
├── components/     # Vue components
├── views/          # Page components
├── router/         # Vue Router
├── store/          # Pinia/Vuex store
├── composables/    # Composables
└── App.vue         # Root component
```

### Next.js (Pages Router)
```
pages/
├── index.js/tsx    # Home page
├── _app.js/tsx     # App component
├── _document.js/tsx # Document wrapper
└── api/            # API routes
```

### Next.js (App Router)
```
app/
├── page.js/tsx     # Home page
├── layout.js/tsx   # Root layout
├── globals.css     # Global styles
└── api/            # API routes
```

### Django
```
myproject/
├── __init__.py
├── settings.py     # Settings
├── urls.py         # URL routing
├── wsgi.py         # WSGI entry
└── asgi.py         # ASGI entry

myapp/
├── models.py       # Data models
├── views.py        # Views
├── urls.py         # App URLs
├── forms.py        # Forms
└── admin.py        # Admin config
```

### Flask
```
myapp/
├── __init__.py     # App factory
├── routes.py       # Route definitions
├── models.py       # Data models
├── templates/      # HTML templates
└── static/         # Static files
```

### Spring Boot
```
src/main/java/
├── com/example/myapp/
│   ├── MyApplication.java    # Main application
│   ├── controller/           # Controllers
│   ├── service/              # Services
│   ├── repository/           # Repositories
│   └── model/                # Models
```

---

## File Extension to Language Mapping

| Extension | Language |
|-----------|----------|
| `.py` | Python |
| `.js` | JavaScript |
| `.jsx` | JavaScript (React) |
| `.ts` | TypeScript |
| `.tsx` | TypeScript (React) |
| `.vue` | Vue |
| `.go` | Go |
| `.rs` | Rust |
| `.java` | Java |
| `.kt`, `.kts` | Kotlin |
| `.c`, `.h` | C |
| `.cpp`, `.hpp` | C++ |
| `.cs` | C# |
| `.swift` | Swift |
| `.rb` | Ruby |
| `.php` | PHP |
| `.scala` | Scala |
| `.dart` | Dart |
| `.lua` | Lua |
| `.r` | R |
| `.m`, `.mm` | Objective-C/Objective-C++ |
| `.sql` | SQL |
| `.sh`, `.bash` | Shell/Bash |
| `.zsh` | Zsh |
| `.ps1` | PowerShell |
