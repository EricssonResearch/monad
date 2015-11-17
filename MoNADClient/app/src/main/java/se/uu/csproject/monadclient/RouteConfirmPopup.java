package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
import se.uu.csproject.monadclient.recyclerviews.Storage;

public class RouteConfirmPopup extends AppCompatActivity implements AsyncResponseString, AsyncResponse, AsyncResponseMulti{

    private TextView busIdView, startTimeView, endTimeView, startPositionView, endPositionView;
    private FullTrip trip;
    private Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_route_confirm);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .40));

        busIdView = (TextView) findViewById(R.id.businfo);
        startTimeView = (TextView) findViewById(R.id.departtime);
        endTimeView = (TextView) findViewById(R.id.arrivetime);
        startPositionView = (TextView) findViewById(R.id.departname);
        endPositionView = (TextView) findViewById(R.id.arrivename);
        context = getApplicationContext();

        Bundle b = getIntent().getExtras();
        trip = b.getParcelable("selectedTrip");

        busIdView.setText(getString(R.string.label_trip_businfo) + " " + trip.getBusLinesString());
        startTimeView.setText(formatTime(trip.getStartTime()));
        endTimeView.setText(formatTime(trip.getEndTime()));
        startPositionView.setText(trip.getStartBusStop());
        endPositionView.setText(trip.getEndBusStop());

        ImageButton cancel = (ImageButton)findViewById(R.id.cancelbutton);
        cancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                //return to the previous activity instead of start a new one
                finish();
            }


        });
    }

    // Book the trip
    public void confirmTrip(View view){
        ArrayList<FullTrip> bookings = Storage.getBookings();

        if (bookings.isEmpty()){
            getBookings();
        } else if (!isAlreadyBooked(trip, bookings)){
            SendBookingRequest asyncTask = new SendBookingRequest();
            asyncTask.delegate = this;
            asyncTask.execute(trip.getId());
        } else {
            CharSequence text = getString(R.string.java_trips_samebooking);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    // Gets the user's bookings from the server
    private void getBookings(){
        String userId = ClientAuthentication.getClientId();
        SendUserBookingsRequestExtra asyncTaskMulti = new SendUserBookingsRequestExtra();
        asyncTaskMulti.delegateMulti = this;
        asyncTaskMulti.execute(userId);
    }

    // Checks if the user has already booked this trip
    private boolean isAlreadyBooked(FullTrip fullTrip, ArrayList<FullTrip> bookings){
        boolean isAlreadyBooked = false;
        ArrayList<PartialTrip> partialTrips;
        PartialTrip partialTripFirst, partialTripLast;

        for (int i = 0; i < bookings.size(); i++){
            partialTrips = bookings.get(i).getPartialTrips();
            partialTripFirst = partialTrips.get(0);
            partialTripLast = partialTrips.get(partialTrips.size() - 1);

            if (partialTripFirst.getStartTime().equals(fullTrip.getStartTime()) &&
                    partialTripLast.getEndTime().equals(fullTrip.getEndTime()) &&
                    partialTripFirst.getStartBusStop().equals(fullTrip.getStartBusStop()) &&
                    partialTripLast.getEndBusStop().equals(fullTrip.getEndBusStop())){
                isAlreadyBooked = true;
                break;
            }
        }

        return isAlreadyBooked;
    }

    // Deals with the response by the server after requesting the user's bookings to check for double bookings
    public void processFinishMulti(ArrayList<FullTrip> bookings){
        Storage.setBookings(bookings);

        if (bookings.isEmpty() || !isAlreadyBooked(trip, bookings)){
            SendBookingRequest asyncTask = new SendBookingRequest();
            asyncTask.delegate = this;
            asyncTask.execute(trip.getId());
        } else {
            CharSequence text = getString(R.string.java_trips_samebooking);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    // Deal with the response from the server after the user books the trip
    public void processFinish(String response){
        Toast toast = Toast.makeText(context, response, Toast.LENGTH_SHORT);
        toast.show();

        String userId = ClientAuthentication.getClientId();
        SendUserBookingsRequest asyncTask = new SendUserBookingsRequest();
        asyncTask.delegate = this;
        asyncTask.execute(userId);
    }

    // Deals with the response by the server after requesting the updated user's bookings
    public void processFinish(ArrayList<FullTrip> bookings){
        Storage.setBookings(bookings);
        Intent intent = new Intent(this, TripsActivity.class);
        startActivity(intent);
        finish();
    }

    private String formatTime(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        return timeFormat.format(calendar.getTime());
    }
}
