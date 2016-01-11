package se.uu.csproject.monadclient.activities;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.storage.FullTrip;
import se.uu.csproject.monadclient.storage.PartialTrip;

public class RouteActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_route);
        Toolbar toolbar = (Toolbar)findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);


//        String name;
        Date timeExit;
        Date timeStart;
        String busStop;
        int line;

        Bundle b = getIntent().getExtras();
        final FullTrip trip = b.getParcelable("selectedTrip");
        ArrayList <PartialTrip> partialTrips = trip.getPartialTrips();
        Button joinTripButton = (Button)findViewById(R.id.button_jointrip);

        if (trip.isReserved()) {
            joinTripButton.setVisibility(View.GONE);
        }

        LayoutInflater vi = (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        ViewGroup insertPoint = (ViewGroup) findViewById(R.id.layout1);

        for(int i = 0 ; i < partialTrips.size(); i++) {
            timeStart = partialTrips.get(i).getStartTime();
            timeExit = partialTrips.get(i).getEndTime();
            line = partialTrips.get(i).getLine();
            ArrayList<String> busStops = partialTrips.get(i).getTrajectory();

            for(int j = 0 ; j < busStops.size(); j++) {
                busStop = busStops.get(j);
                View busStopView;
                TextView time;
                TextView instructions;

                if (j > 0 && j < busStops.size() - 1) {
                    busStopView = vi.inflate(R.layout.route_details, insertPoint, false);
                    busStop = "\u2022 " + busStop;
                } else {
                    busStopView = vi.inflate(R.layout.bus_stop, insertPoint, false);
                    time = (TextView) busStopView.findViewById(R.id.exit_time);
                    instructions = (TextView) busStopView.findViewById(R.id.label_instructions);

                    if (j == 0) {
                        time.setText(formatTime(timeStart));
                        instructions.setText(String.format(getString(R.string.java_route_board),line));
                    } else {
                        ImageView busStopImage = (ImageView) busStopView.findViewById(R.id.bus_stop_image);
                        time.setText(formatTime(timeExit));
                        busStopImage.setVisibility(View.INVISIBLE);
                        instructions.setText(getString(R.string.label_trip_arrive));
                    }
                }

                TextView textBusStop = (TextView) busStopView.findViewById(R.id.bus_stop);
                textBusStop.setText(busStop);
                insertPoint.addView(busStopView);
            }
        }

        joinTripButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                Intent myIntent = new Intent(RouteActivity.this, RouteConfirmPopup.class);
                myIntent.putExtra("selectedTrip", trip);
                RouteActivity.this.startActivity(myIntent);
            }
        });
    }

    private String formatTime(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        return timeFormat.format(calendar.getTime());
    }

}
