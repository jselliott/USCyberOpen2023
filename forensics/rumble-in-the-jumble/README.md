# Rumble In The Jumble

We've received an important executable file from a company that were victims of a ransomware attack. It appears that the file is all jumble up but we can't quite figure out how! If you are somehow able to recover the file I'm sure you'll be rewarded! (With a flag)

## Provided File

* [jumble](jumble)

## Solution

The alphanumeric bytes of the executable have all been swapped out (while still maintaining the same case) but players can attempt to begin to find a substitution cipher by searching for known C strings, etc. Starting with something like the ELF header at the top, then looking and seeing the jumbled flag in memory they can figure out the mapping for "USCG", etc. Then they can look for common strings added by the compiler by comparing other C programs. Eventually the substitution will get easier as they discover more mapping until the entire thing unravels the flag is revealed.