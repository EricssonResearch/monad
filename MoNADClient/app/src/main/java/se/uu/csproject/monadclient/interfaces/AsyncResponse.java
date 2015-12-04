package se.uu.csproject.monadclient.interfaces;


import java.util.ArrayList;

import se.uu.csproject.monadclient.storage.FullTrip;

public interface AsyncResponse {

    void processFinish(ArrayList<FullTrip> searchResults);
}
