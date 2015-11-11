package se.uu.csproject.monadclient;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.MenuItem;
import android.widget.Toast;

import java.util.ArrayList;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.Storage;
import se.uu.csproject.monadclient.recyclerviews.TripRecyclerViewAdapter;


public class TripsActivity extends MenuedActivity implements AsyncResponse{
    private Toolbar toolbar;
    private Context context;
    private RecyclerView recyclerView;
    private LinearLayoutManager linearLayoutManager;
    private TripRecyclerViewAdapter adapter;
    private ArrayList<FullTrip> bookings;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trips);
        context = getApplicationContext();
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        recyclerView = (RecyclerView) findViewById(R.id.recycler_view_active);
        linearLayoutManager = new LinearLayoutManager(context);
        recyclerView.setLayoutManager(linearLayoutManager);

        setSupportActionBar(toolbar);
        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);
    }

    @Override
    protected void onResume() {
        super.onResume();
        bookings = Storage.getBookings();
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
            CharSequence text = "You haven't booked any trips.";
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        } else {
            adapter = new TripRecyclerViewAdapter(bookings);
            recyclerView.setAdapter(adapter);
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if(id == R.id.action_mytrips){
            return true;
        }
        else {
            return super.onOptionsItemSelected(item);
        }
    }
}