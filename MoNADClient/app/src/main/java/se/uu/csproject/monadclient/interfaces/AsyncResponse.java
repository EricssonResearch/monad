package se.uu.csproject.monadclient.interfaces;


import java.util.ArrayList;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;

public interface AsyncResponse {

    void processFinish(ArrayList<FullTrip> searchResults);
}
