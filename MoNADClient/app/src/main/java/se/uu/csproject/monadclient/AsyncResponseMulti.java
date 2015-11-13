package se.uu.csproject.monadclient;


import java.util.ArrayList;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;

public interface AsyncResponseMulti {

    void processFinishMulti(ArrayList<FullTrip> results);
}
