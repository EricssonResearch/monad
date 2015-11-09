package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.TripRecyclerViewAdapter;


public class TripsActivity extends MenuedActivity implements AsyncResponse{
    private Toolbar toolbar;
    private ImageButton button;
    private Context context;

    //TODO Ilyass: (high priority) Make specific trips selectable
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trips);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);
        context = getApplicationContext();

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        getBookings();
    }

    private void getBookings(){
        String userId = ClientAuthentication.getClientId();
        SendUserBookingsRequest asyncTask = new SendUserBookingsRequest();
        asyncTask.delegate = this;
        asyncTask.execute(userId);
    }

    public void processFinish(ArrayList<FullTrip> bookings){
        if (bookings.isEmpty()){
            CharSequence text = "You haven't booked any trips.";
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        } else {
            RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view_active);
            LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getApplicationContext());
            recyclerView.setLayoutManager(linearLayoutManager);
            TripRecyclerViewAdapter adapter = new TripRecyclerViewAdapter(bookings);
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