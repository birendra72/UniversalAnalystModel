import cProfile
import pstats
import data_loader_cli as dl

with cProfile.Profile() as pr:
    dl.main()  # Your main function

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME).print_stats(20)