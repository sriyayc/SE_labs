# Lab 5 Reflection

Name: Sriya
SRN: PES2UG24CS523

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The Flake8 ones were the easiest, like long lines, extra blank lines and missing spaces around `=`. They are just formatting and don't change what the code does. The hardest one was the `global` warning from Pylint. I had to think of another way to keep the service count without `global`, so I put it in a dict. Removing pickle also needed a bit of thought, because first I had to understand why it was there. It was only copying the rows, so a normal list was enough.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

The hardcoded password warning (B105) is a bit of a false positive here, because the password is never actually used anywhere in the program. Still, it's bad practice to keep passwords in code, so I moved it to an environment variable anyway. Bandit also gave B403 just for importing pickle, which on its own isn't dangerous. The real problem was `pickle.loads` (B301).

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint in a pre-commit hook so problems are caught before the code is even committed. In CI (like GitHub Actions) I would run all three tools on every pull request and fail the build if Bandit finds Medium or High issues or the Pylint score goes below a set limit, like 9.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 5.14 to 10.00, and Bandit and Flake8 show no issues now. The SQL is safe from injection, and the code no longer uses pickle or keeps a password in the file. Names follow snake_case and every function has a docstring, so it's easier to read. While fixing, I also found two real bugs that the tools didn't point out directly: `risk_level` crashed when the tower id did not exist, and `service_tower` never committed its update.
