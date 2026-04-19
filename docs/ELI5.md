# Explain Like I'm Five

← [Back to the technical version](../README.md)

---

## What is this?

Someone on the internet built a thing that tries to predict whether the US stock market will go up or down based on **Donald Trump's Truth Social posts**. They say it's right 61% of the time — which, if true, is a big deal. They published all their code and data on GitHub, so anyone can look at it.

We wanted to find out: **does that actually work for a regular person with $1,000?** And if not, **why not?**

Their test was on the stock market. But betting on the US stock market the way a big Wall Street firm does is expensive and slow for a regular person. So we tested whether the same signals work on **Polymarket** — a website where people bet real money on whether specific things will happen (like "Will Trump resign by the end of 2026?"). Polymarket is easier for a person sitting at home to actually trade on.

## What were we trying to do?

Three specific questions:

1. **Does their 61% number actually reproduce?** Or did we misread their files, or did they quietly round up? We wanted to recompute it ourselves from the raw data, with our own code, and see if we got the same number.

2. **Is the 61% real or is it cheating?** When you get a "prediction" that's really a "report on something that already happened," the stats can look amazing but the trader can never actually capture that money. We wanted to check whether their 61% was real prediction or disguised reporting.

3. **If it's real, does it work on Polymarket?** The whole point. Can a person with $1,000 use Trump's posts to find good bets on Polymarket's political markets?

## What did we do?

We picked a 10-day budget and made ourselves write down **all our rules in advance**, before touching any data. This is called pre-registration. The point is to stop ourselves from quietly moving the goalposts when the answer starts looking bad.

We wrote down:
- Exactly which 5 of their "rules" we'd test
- Exactly which 10 Polymarket betting markets we'd test them on
- Exactly what counts as "working" (a hit rate of at least 55%, a profit of at least 2% per trade after fees, and four other specific things)
- Exactly when we'd give up and say "this doesn't work"

Then we ran the 10 days. Each day had its own checkpoint — if a certain test failed, we'd stop right there and not waste effort.

## What did we find?

### Day 2 — does the 61% reproduce?

**Yes.** We recomputed it from scratch and got **61.35%** — matches their published number to two decimal places. Their files are readable and their math is right.

### Day 3 — is it real prediction or disguised reporting?

**Mostly real, but with an asterisk.** About 26% of their "correct" predictions are ones where the stock market had already moved *before* Trump's post could have fired the signal. So roughly 1 in 4 of their "wins" is actually measuring something that already happened.

This is just below the line we'd set (30%) for calling the whole thing cheating. So we kept going, but with a yellow flag on the strongest-seeming of their rules.

### Days 4–7 — does it work on Polymarket?

**No.** We tested 5 of their rules on 10 Polymarket markets, two different ways each = 100 tests. **Zero** passed our pre-registered bar.

In particular:
- The one rule with enough data to really test (the "burst then silence" rule, which is the biggest contributor to their 61%) landed at **24.6% hit rate** on Polymarket, vs **26.1% baseline**. So slightly worse than just guessing. Not better.
- Some other rules showed *hints* of something working, but every one of them was too small a sample to trust. Like "we won 3 out of 4" small.

### Day 9 — the verdict

**KILL.** Don't continue to live trading. Don't deploy capital. The signal doesn't translate.

## Wait, did their 61% number get debunked then?

**No.** That's important. We confirmed that:
- We can read their files correctly (we get 61.35%, matches)
- Their math on S&P 500 does what they say it does
- There's some real predictive signal there, not pure reporting

What we showed is narrower: **when we take 5 of their rules and point them at 10 specific Polymarket political markets with +1-day and +3-day horizons, no combination produces enough edge for a regular person to trade profitably.**

Their stock-market claim might still be real. Their signal might still work on other markets, at other horizons, with more data. We didn't test any of that — and we were very careful to say so.

## Was there anything left standing?

One rule we couldn't kill but also couldn't prove: **"B1" — the 4-signals-in-a-row rule.**

This one is interesting because:
- It's the one rule where the "disguised reporting" problem basically doesn't apply (it's a 3-day bet, so the entry timing doesn't matter much)
- On the few Polymarket markets where we had enough data, it hit **66–78%** — which would be very impressive if we had more observations
- But we only ever had 4–9 observations per market. That's too few to be sure.

So B1 isn't dead. It's just underpowered. Someone running this experiment with more data (say, 2× the time window) could get a real answer on B1 specifically. We did not.

## So was the whole thing pointless?

No. A few useful things came out of it:

### 1. A careful honest "no, this doesn't work (yet)"

Most people publish wins and bury failures. This whole repo is what a **disciplined negative result** looks like. Someone else thinking of building the same thing can read this in 30 minutes and save themselves a few weeks.

### 2. A paper trail of Polymarket's weird quirks

Polymarket's data APIs have several undocumented gotchas — broken timestamp filters, pagination caps, weird fee structures — that would silently cost a trader real money if they hit them without warning. We wrote them all down in the [main README](../README.md) under "Polymarket findings observed."

### 3. Evidence about the original claim that's stronger than what they published

Their headline number is "61.3% hit rate." That's just an accuracy number — it doesn't tell you whether the signal is **predictive** or **reporting-in-disguise**. We did the work to separate those. Result: about 26% reporting contamination in aggregate, much higher for some specific rules. That's a more honest and useful characterisation than the headline alone.

### 4. Rules that generalise

These apply to anyone evaluating "AI found a pattern that beats the market" claims:

- **Reproduce the headline number first.** If you can't get the same number from the same data, you've misread something. Don't go further.
- **Separate "prediction" from "reporting."** Any time you see a performance number, ask: could the trader have acted on this in time?
- **Pre-register your test.** Write down what counts as "working" before you see the answer. Otherwise you'll always find a way to make the answer look good.
- **Underpowered ≠ falsified.** If you couldn't gather enough data to tell, the honest answer is "we don't know yet," not "it doesn't work." Mark those separately.

## What about using AI to help?

Same note as the [parent project](../../event-impact-mvp/docs/ELI5.md): the AI is great at **sounding** right, and occasionally actually is.

One specific thing that kept happening in this project: when numbers landed near a decision line (our lag-contamination was 25.9% vs a 30% cutoff; our p-values were borderline), the AI's natural tendency was to argue for whichever side I'd been leaning. That's why the discipline of writing the **counter-memo** before the verdict matters — it forces the AI to argue against itself from the same data, not with itself.

## So what's the big-picture lesson?

Three things:

1. **"61% hit rate on S&P" doesn't automatically become "61% hit rate on Polymarket."** Signals don't port between venues for free. The structure of the market you're trading on changes what kind of edge is capturable. This one doesn't port — at least not in the form and horizons we tested.

2. **One rule (B1) survived but couldn't be proved.** The honest verdict is "underpowered, not falsified," not "doesn't work." If you ever see a person or AI conflate those two, they're being sloppy.

3. **Pre-registration is the thing that made this trustworthy.** Without it, we could easily have drifted into "well, actually C1 looks pretty good if we just change the threshold a bit." With it, the KILL verdict is defensible — anyone can audit the git log and see the thresholds were set before the data was measured.

---

← [Back to the technical version](../README.md)
