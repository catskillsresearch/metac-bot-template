import os
from list_active_ifps import list_active_ifps
from save_ifps_to_disk import save_ifps_to_disk
from forecast_ifp import forecast_ifp
from gather_news_for_ifps import gather_news_for_ifps

def glimt_bot():
    os.makedirs('glimt/prompt', exist_ok=True)
    ifps = list_active_ifps()
    id_to_ifp = save_ifps_to_disk(ifps)
    news = gather_news_for_ifps(ifps)
    for ifp in ifps:
        if ifp['id'] == 469:
            forecast_ifp(ifp, news)
            return

if __name__ == "__main__":
    while True:
        glimt_bot()
        quit()