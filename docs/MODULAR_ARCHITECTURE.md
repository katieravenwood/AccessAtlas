# AccessAtlas Modular Architecture

AccessAtlas publishes a quick-start single-file application from one canonical modular codebase and keeps the hosted demo as a separate runtime.

## Distribution and runtime model

```text
                         modular/accessatlas/app_core.py
                                      |
                     shared workflows and application UI
                                      |
                   +------------------+------------------+
                   |                                     |
                   v                                     v
      build_starter_runtime()                build_demo_runtime()
                   |                                     |
                   v                                     v
          modular/app.py                       modular/demo_app.py
                   |                                     |
                   | canonical starter                    | hosted demo
                   v                                     v
      tools/build_single_file.py              Streamlit demo deployment
                   |
                   v
              root app.py
```

The application UI and business logic are shared.

The runtime determines:

- the current application identity
- role-visible sections
- visible user, system, access, and administrator records
- optional runtime-specific guidance

## Root `app.py`: quick-start starter

The root application is generated from the modular starter runtime.

It contains no:

- Demo Mode persona selector
- Demo Mode sidebar warning
- Current Demo User panel
- Visible Demo Scope panel
- demo-only contextual sidebar guidance

Run it with:

```bash
streamlit run app.py
```

The starter resolves its current application identity from the `ACCESSATLAS_USER_ID` environment variable.

Example:

```bash
ACCESSATLAS_USER_ID=USR-0001 streamlit run app.py
```

When the variable is not set, the reference dataset resolves the first active Super Administrator, then the first active user, as a development-friendly fallback.

This is an application identity placeholder, not authentication. Production implementations should replace the starter runtime with an approved authentication provider and enforce authorization in the backend and data-access layer.

## `modular/demo_app.py`: hosted demo

The hosted demo retains the synthetic persona selector and role-scoped preview experience.

Run it with:

```bash
streamlit run modular/demo_app.py
```

The demo includes:

- Demo Mode explanation
- synthetic user/persona selector
- current demo user summary
- visible demo scope summary
- contextual sidebar guidance
- role-aware record and section scoping

Tester changes continue to use Streamlit session state and reset with the demo session.

## Shared application core

`modular/accessatlas/app_core.py` owns the shared Streamlit workflows and rendering logic.

It receives a runtime factory:

```python
run_app(build_starter_runtime)
```

or:

```python
run_app(build_demo_runtime)
```

The core does not own identity selection or demo controls.

This prevents the starter and demo from becoming separate application implementations.

## Runtime context

`modular/accessatlas/runtime.py` defines `RuntimeContext`.

A runtime context supplies:

```text
current_user
visible_tabs
users
systems
access
system_admins
runtime_name
is_demo
section_guidance_renderer
```

Future authentication modules can resolve the same context contract without rewriting workflow pages.

## Runtime implementations

### `starter_runtime.py`

Provides the clean starter behavior.

It:

1. resolves the configured application identity;
2. determines visible sections from the application role;
3. applies the current role-scope rules; and
4. returns a runtime context without demo UI.

### `demo_runtime.py`

Provides the hosted preview behavior.

It:

1. renders the persona selector;
2. resolves the selected synthetic user;
3. determines visible sections;
4. applies the same role-scope rules used by the starter;
5. renders demo scope information; and
6. attaches demo-only contextual guidance.

## Single-file publishing

The modular implementation remains the canonical engineering source.

Build the root starter with:

```bash
python tools/build_single_file.py
```

Verify synchronization with:

```bash
python tools/build_single_file.py --check
```

The generated root `app.py` bundles:

- shared application modules
- runtime context
- starter runtime
- shared application core
- starter entry point

The demo runtime is deliberately excluded from the generated root application.

## Hosted demo deployment

The Streamlit-hosted preview should use:

```text
modular/demo_app.py
```

The root `app.py` should remain the recommended quick-start path in the README.

## Maintenance rule

Shared application changes belong in:

```text
modular/accessatlas/
```

Starter runtime behavior belongs in:

```text
modular/accessatlas/starter_runtime.py
```

Demo-only behavior belongs in:

```text
modular/accessatlas/demo_runtime.py
```

After shared or starter changes:

```bash
python tools/build_single_file.py
```

Commit the modular source and generated root `app.py` together.

Demo-only changes do not require rebuilding root `app.py` unless shared application behavior also changed.
