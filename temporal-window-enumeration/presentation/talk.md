# How much time can you recover from a clock?

**Opening (30 seconds).** Imagine arriving in front of a clock that shows just one of three symbols. You know the sequence the clock follows, and you know it repeats every 24 ticks. What you have lost is your place in that sequence. How long do you need to watch before you know the time?

**A concrete answer (40 seconds).** Design the clock so each symbol appears eight times. One observation leaves eight possible phases. Two consecutive observations narrow the possibilities to two or three, and three observations identify the phase exactly. Now ask how many different clocks do this, counting clocks that begin at different points on the same cycle just once. The candidate theorem gives 148,608.

**Where the proof turns (50 seconds).** Three symbols make 27 possible three-symbol windows. The 24-tick clock uses 24 of them. Follow the three missing windows. Each observed transition enters and leaves a context, and a whole period returns to its beginning. That conservation applies to the missing transitions too. In the general construction, short contexts distinguish them, and following one missing transition to the next gives a permutation.

**What generalizes (35 seconds).** Fix the number of missing windows and let the identifying window get longer. The clock grows exponentially. The matrix needed for each term of the exact count keeps the same size, determined by how many windows are missing. The theorem also specifies how the normalized count approaches a limit.

**Closing (25 seconds).** This is a result about information available to an observer who knows the clock. The phase evolves reversibly, and the window determines exactly how much of the temporal position can be recovered. The proof is written and 26 finite cases were verified computationally. Independent verification and confirmation of publication priority remain open.
