# Mission GroundWork Media Pack

This repository owns Mission GroundWork product truth, audience, approved claims, brand direction, and final media approval. It consumes the cross-portfolio `MCLP-001` process contract; this repository does not own portfolio-wide media generation.

## Current media lane

- Process version: `MCLP-001 / 0.3.1-phase-3-local-resume`
- Current canary: `IMG-004`
- Method: deterministic editorial photography
- Structured job: `media/jobs/IMG-004-ownership-is-fuzzy.json`
- Renderer: `scripts/render_mclp_img_004.py`
- Production state: technical and provisional creative pass; owner review required
- Publishing: disabled
- Paid services: disabled

## Local contract

Media must remain grounded, warm, credible, spacious, and evidence-led. Human photography or illustration is used only where it adds context. Unsupported clients, testimonials, outcomes, demand, scarcity, or availability claims are prohibited.

The primary conversion action is **Request a GroundWork session**. Media may support recognition, authority, education, proof, or conversion only when the destination and supporting evidence exist.

## Smoke test

The repository workflow `.github/workflows/media-smoke-test.yml` verifies that the local MCLP declaration, project and quality profiles, toolchain lock, output index, structured canary job, renderer, and publishing boundary remain present and internally consistent.

## Output custody

Generated review artifacts remain private GitHub Actions artifacts unless separately approved. Production outputs must be indexed in `.media/output-index.json`; rejected attempts remain evidence but do not count toward the portfolio target.
