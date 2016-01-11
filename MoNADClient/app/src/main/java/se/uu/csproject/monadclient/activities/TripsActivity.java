package se.uu.csproject.monadclient.activities;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.MenuItem;
import android.widget.Toast;

import org.json.JSONObject;

import java.util.ArrayList;

import se.uu.csproject.monadclient.ClientAuthentication;
import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.interfaces.AsyncResponse;
import se.uu.csproject.monadclient.interfaces.AsyncResponseString;
import se.uu.csproject.monadclient.storage.FullTrip;
import se.uu.csproject.monadclient.storage.Storage;
import se.uu.csproject.monadclient.recyclerviews.TripRecyclerViewAdapter;
import se.uu.csproject.monadclient.serverinteractions.SendUpdateFeedbackRequest;
import se.uu.csproject.monadclient.serverinteractions.SendUserBookingsRequest;


public class TripsActivity extends MenuedActivity implements AsyncResponse, AsyncResponseString {
    private Context context;
    private RecyclerView recyclerView;
    private TripRecyclerViewAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trips);
        context = getApplicationContext();
        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        recyclerView = (RecyclerView) findViewById(R.id.recycler_view_active);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(context);
        recyclerView.setLayoutManager(linearLayoutManager);

        setSupportActionBar(toolbar);
        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);
    }

    @Override
    protected void onResume() {
        super.onResume();
        ArrayList<FullTrip> bookings = Storage.getBookings();
        if (bookings.isEmpty()){
            getBookings();
        } else {
            adapter = new TripRecyclerViewAdapter(bookings);
            recyclerView.setAdapter(adapter);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    @Override
    protected void onStop() {
        super.onStop();

        JSONObject changedFeedback = Storage.getChangedFeedback();
        if (changedFeedback.length() != 0){
            SendUpdateFeedbackRequest asyncTask = new SendUpdateFeedbackRequest();
            asyncTask.delegate = this;
            asyncTask.execute(changedFeedback.toString());
        }
    }

    public void processFinish(String response){
        Storage.clearChangedFeedback();
    }

    // Gets the user's bookings from the server
    private void getBookings(){
        String userId = ClientAuthentication.getClientId();
        SendUserBookingsRequest asyncTask = new SendUserBookingsRequest();
        asyncTask.delegate = this;
        asyncTask.execute(userId);
    }

    // Deals with the response by the server
    public void processFinish(ArrayList<FullTrip> bookings){
        if (bookings.isEmpty()){
            CharSequence text = getString(R.string.java_trips_notripsbooked);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        } else {
            Storage.setBookings(bookings);
            adapter = new TripRecyclerViewAdapter(bookings);
            recyclerView.setAdapter(adapter);
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        return item.getItemId() == R.id.action_mytrips || super.onOptionsItemSelected(item);
    }
}