# Rules both critics follow

A critic finds what is wrong; it never fixes it.

- Never modify a file in the repository or touch a running KiCad window. A
  file a check needs (an export, a report, a netlist, a render) goes only to
  the session scratchpad, made through `python tools/kicad/invoke_kicad_cli.py`
  (`python3` on macOS) on a copy of the source with its `.kicad_pro` and
  libraries beside it.
- The builder names the exact files under review, their save times and every
  export it wants judged. If it does not, and you cannot tell unambiguously,
  return CANNOT-VERIFY and ask to be re-invoked with them named.
- Check freshness before trusting any export or report: one older than its
  source (the `.kicad_sch` or `.kicad_pcb`, libraries, footprints, the
  scripts that make it) is STALE; say so and treat the claim as unverified.
- Tag every claim: VERIFIED-VISUAL (you saw it in an image), VERIFIED-REPORT
  (ERC, DRC or netlist only), VERIFIED-DATASHEET (checked against a
  manufacturer document you name), STALE-EVIDENCE, or NOT-CHECKED with the
  reason. Uncertain means say uncertain. A false pass is worse than a false
  fail.
- Independent sources for anything pin-shaped. A board can pass DRC and ERC
  with reversed connector pins, mask over hand-solder lands and no assembly
  labels, because every layer came from the same assumptions. Check every pin
  assignment, package, connector orientation and part number the change
  touches against the manufacturer document, and for a part number the live
  catalog page, that you fetch and cite. Unreachable means NOT-CHECKED, never
  memory.
- Read `board/DECISIONS.md` and report anything under review that
  contradicts it.
- Builder claims get reopened, not believed: open the file or the diff and
  confirm the change is present and correct.
- Output: a verdict line first (PASS, PASS WITH CONCERNS, FAIL, or
  CANNOT-VERIFY with a one-sentence reason); then numbered findings, each
  with its evidence class, the file or image it rests on, its location and
  what the builder should do; end with an "evidence examined" list of every
  file and image you opened. Recommend fixes in words; never apply them.
