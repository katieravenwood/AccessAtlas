# README Update for Starter and Demo Runtimes

Suggested replacement content for the README implementation-path and local-run sections.

## Choose an Implementation Path

AccessAtlas uses one shared modular application core with separate starter and demo runtimes.

### Quick-start single-file application

The root-level `app.py` is the recommended starting point for organizations that want to inspect, edit, and run AccessAtlas with minimal application-architecture overhead.

```bash
streamlit run app.py
```

The quick-start application does not include the hosted demo persona selector or demo sidebar.

The starter currently resolves its application identity from `ACCESSATLAS_USER_ID`. This is a development/configuration placeholder rather than authentication.

### Modular implementation

The canonical engineering source is under:

```text
modular/
```

Run the clean modular starter with:

```bash
streamlit run modular/app.py
```

Use this implementation when adding authentication, persistence adapters, notifications, audit workflows, provisioning integrations, or broader tests.

### Hosted demo

The public preview uses:

```bash
streamlit run modular/demo_app.py
```

The demo retains the synthetic persona selector and role-aware preview experience so visitors can explore AccessAtlas from different governance roles.

Demo changes remain session-backed and are not persisted.

### Publishing the quick-start application

The root `app.py` is generated from the modular starter:

```bash
python tools/build_single_file.py
```

Verify synchronization with:

```bash
python tools/build_single_file.py --check
```

Make shared application changes under `modular/accessatlas/`, then rebuild and commit the root quick-start file with the canonical modular source.
