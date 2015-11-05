package se.uu.csproject.monadclient;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;

public class RouteConfirmPopup extends AppCompatActivity {

    private FullTrip trip;
    private TextView busIdView;
    private TextView startTimeView;
    private TextView endTimeView;
    private TextView startPositionView;
    private TextView endPositionView;

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

        Bundle b = getIntent().getExtras();
        trip = b.getParcelable("selectedTrip");

        busIdView.append(trip.getBusLines());
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

    public void confirmTrip(View view){
        String busId, busIdText[], startTime, startTimeText, endTime, endTimeText, stPosition, edPosition, userId;
        int currentYear, currentMonth, currentDay;
        Calendar rightNow = Calendar.getInstance();

        currentYear = rightNow.get(Calendar.YEAR);
        currentMonth = rightNow.get(Calendar.MONTH);
        // Genius design choice: months are numbered 0-11
        currentMonth++;
        currentDay = rightNow.get(Calendar.DAY_OF_MONTH);

        busIdText = ( busIdView.getText().toString() ).split("\\s+");
        busId = busIdText[1];
        userId = ClientAuthentication.getClientId();
        startTimeText = startTimeView.getText().toString();
        startTime = currentYear + " " + currentMonth + " " + currentDay + " " + startTimeText;
        endTimeText = endTimeView.getText().toString();
        endTime = currentYear + " " + currentMonth + " " + currentDay + " " + endTimeText;
        stPosition = startPositionView.getText().toString();
        edPosition = endPositionView.getText().toString();

        //new SendBookingRequest().execute(busId, userId, startTime, endTime, stPosition, edPosition);
        Intent intent = new Intent(RouteConfirmPopup.this, TripsActivity.class);
        //intent.putExtra("selectedTrip", trip);
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
