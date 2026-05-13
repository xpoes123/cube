"""Cube CLI. Subcommands: ingest, stats."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from cube.corpus import validate
from cube.corpus.record import segmented_to_dict
from cube.corpus.sources.api333fm import (
    Api333fmClient,
    submission_to_reconstruction,
)
from cube.segmenter import segment


def cmd_ingest(args: argparse.Namespace) -> int:
    """Walk WCA reconstructions via the 333.fm API, validate, segment, write JSONL."""
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)

    client = Api333fmClient(cache_dir=cache_dir, delay_sec=args.delay)
    stats = {
        "total_submissions": 0,
        "parsed": 0,
        "validated": 0,
        "segmented_from_comment": 0,
        "validation_failures": [],
        "by_method": Counter(),
        "by_phase_label": Counter(),
    }

    written = 0
    with out_path.open("w") as f:
        for comp_summary in client.iter_wca_competitions():
            wca_id = comp_summary.get("wcaCompetitionId")
            if not wca_id:
                continue
            comp_data = client.get_competition(wca_id)
            comp_name = comp_data.get("competition", {}).get("name", wca_id)
            for recon in comp_data.get("recons", []):
                user_id = recon.get("userId")
                if user_id is None:
                    continue
                user_data = client.get_user_submissions(wca_id, user_id)
                for sub in user_data.get("submissions", []):
                    stats["total_submissions"] += 1
                    rec = submission_to_reconstruction(
                        sub,
                        recon=user_data.get("recon", recon),
                        competition_name=comp_name,
                        stats=client.stats,
                    )
                    if rec is None:
                        continue
                    stats["parsed"] += 1

                    val = validate(rec)
                    if not val.ok:
                        stats["validation_failures"].append(
                            {"id": rec.source_id, "reason": val.reason}
                        )
                        if not args.keep_invalid:
                            continue
                    else:
                        stats["validated"] += 1

                    seg = segment(rec)
                    if seg.source == "comment":
                        stats["segmented_from_comment"] += 1
                    stats["by_method"][seg.method.value] += 1
                    for s in seg.segments:
                        stats["by_phase_label"][s.raw_label or "(none)"] += 1

                    f.write(json.dumps(segmented_to_dict(seg), ensure_ascii=False) + "\n")
                    written += 1
                    if args.limit and written >= args.limit:
                        client.close()
                        _print_summary(stats, written, out_path)
                        return 0

    client.close()
    _print_summary(stats, written, out_path)
    return 0


def _print_summary(stats: dict, written: int, out_path: Path) -> None:
    print(f"\nWrote {written} records to {out_path}")
    print(f"  Total submissions seen:        {stats['total_submissions']}")
    print(f"  Parsed into Reconstruction:    {stats['parsed']}")
    print(f"  Engine-validated:              {stats['validated']}")
    print(f"  Segmented from author comment: {stats['segmented_from_comment']}")
    print(f"  Validation failures:           {len(stats['validation_failures'])}")
    print(f"\nBy method:")
    for method, n in stats["by_method"].most_common():
        print(f"  {n:5d}  {method}")
    print(f"\nTop 15 raw phase labels:")
    for label, n in stats["by_phase_label"].most_common(15):
        print(f"  {n:5d}  {label!r}")
    if stats["validation_failures"]:
        print(f"\nFirst 5 validation failures:")
        for f in stats["validation_failures"][:5]:
            print(f"  {f['id']}: {f['reason']}")


def cmd_baseline(args: argparse.Namespace) -> int:
    """Train and evaluate non-ML baselines on the corpus."""
    from cube.training import iter_examples_from_jsonl, split_by_source_id
    from cube.training.baselines import (
        BigramBaseline,
        BigramPhaseBaseline,
        FrequencyBaseline,
        PhaseFrequencyBaseline,
        accuracy,
        topk_accuracy_baseline,
    )

    path = Path(args.input)
    if not path.exists():
        print(f"No corpus at {path}", file=sys.stderr)
        return 1

    examples = list(iter_examples_from_jsonl(path))
    if not examples:
        print("Corpus is empty", file=sys.stderr)
        return 1

    source_ids = sorted({ex.source_id for ex in examples})
    train_sids, val_sids, _test_sids = split_by_source_id(source_ids)

    train = [ex for ex in examples if ex.source_id in train_sids]
    val = [ex for ex in examples if ex.source_id in val_sids]

    print(f"Total examples: {len(examples)} from {len(source_ids)} solves")
    print(f"  Train: {len(train)} examples ({len(train_sids)} solves)")
    print(f"  Val:   {len(val)} examples ({len(val_sids)} solves)")

    models: list[tuple[str, object]] = [
        ("Frequency (global)", FrequencyBaseline()),
        ("Frequency (per-phase)", PhaseFrequencyBaseline()),
        ("Bigram", BigramBaseline()),
        ("Bigram + phase", BigramPhaseBaseline()),
    ]

    print(f"\n{'Model':<22s} {'Train top-1':>12s} {'Val top-1':>10s} {'Val top-3':>10s} {'Val top-5':>10s}")
    print("-" * 70)
    for name, model in models:
        model.fit(train)
        train_acc = accuracy(model, train)
        val_acc = accuracy(model, val)
        val_top3 = topk_accuracy_baseline(model, val, k=3)
        val_top5 = topk_accuracy_baseline(model, val, k=5)
        print(f"{name:<22s} {train_acc:>12.3f} {val_acc:>10.3f} {val_top3:>10.3f} {val_top5:>10.3f}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Print stats on an existing JSONL corpus."""
    path = Path(args.input)
    if not path.exists():
        print(f"No corpus at {path}", file=sys.stderr)
        return 1
    methods = Counter()
    phases = Counter()
    canonical = Counter()
    lengths = []
    target_moves = Counter()
    has_comment = 0
    n = 0
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            n += 1
            methods[r.get("method", "?")] += 1
            lengths.append(r.get("length", 0))
            if r.get("commentary"):
                has_comment += 1
            for phase in r.get("phases", []):
                canonical[phase["phase"]] += 1
                phases[phase["raw_label"] or "(none)"] += 1
            # Move frequency in the post-insertion flat solution.
            for token in (r.get("solution_normal") or "").split():
                target_moves[token] += 1
            for token in (r.get("solution_inverse") or "").split():
                target_moves[token] += 1

    print(f"{n} records in {path}")
    if lengths:
        avg = sum(lengths) / len(lengths)
        print(f"Length: min={min(lengths)} avg={avg:.1f} max={max(lengths)}")
    print(f"Has commentary: {has_comment}/{n}")
    print(f"\nMethods: {dict(methods)}")
    print(f"\nCanonical phases: {dict(canonical.most_common())}")
    print(f"\nTop 20 raw labels:")
    for label, count in phases.most_common(20):
        print(f"  {count:5d}  {label!r}")
    print(f"\nTop 15 moves in solutions:")
    for move, count in target_moves.most_common(15):
        print(f"  {count:5d}  {move}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cube", description="FMC analysis tools")
    sub = p.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Pull WCA reconstructions from 333.fm into JSONL")
    p_ingest.add_argument("--output", "-o", default="data/raw/wca.jsonl",
                          help="Output JSONL path (default: data/raw/wca.jsonl)")
    p_ingest.add_argument("--cache-dir", default="data/cache/333fm",
                          help="On-disk cache for API responses")
    p_ingest.add_argument("--delay", type=float, default=0.5, help="Per-request delay (sec)")
    p_ingest.add_argument("--limit", type=int, default=None,
                          help="Stop after N records (for quick iteration)")
    p_ingest.add_argument("--keep-invalid", action="store_true",
                          help="Include records that fail engine validation (default: drop)")
    p_ingest.set_defaults(func=cmd_ingest)

    p_stats = sub.add_parser("stats", help="Report stats on an ingested JSONL corpus")
    p_stats.add_argument("--input", "-i", default="data/raw/wca.jsonl")
    p_stats.set_defaults(func=cmd_stats)

    p_baseline = sub.add_parser(
        "baseline", help="Train + evaluate non-ML baselines on the corpus"
    )
    p_baseline.add_argument("--input", "-i", default="data/raw/wca.jsonl")
    p_baseline.set_defaults(func=cmd_baseline)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
