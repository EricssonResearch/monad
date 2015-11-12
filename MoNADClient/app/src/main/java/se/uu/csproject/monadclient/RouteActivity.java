package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.TypedValue;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
//import se.uu.csproject.monadclient.recyclerviews.Notify;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
//import se.uu.csproject.monadclient.recyclerviews.RouteRecyclerViewAdapter;

public class RouteActivity extends AppCompatActivity {

    RecyclerView recycler;
    boolean flagListVisible = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_route);
        Toolbar toolbar = (Toolbar)findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);


        String name;
        Date exit;
        Date time;
        String busStop;

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
            name = partialTrips.get(i).getStartBusStop();
            time = partialTrips.get(i).getStartTime();
            exit = partialTrips.get(i).getEndTime();
            ArrayList<String> busStops = partialTrips.get(i).getTrajectory();

//            View v = vi.inflate(R.layout.route_details, null);
//
//            TextView stopTime = (TextView) v.findViewById(R.id.label_first_time);
//            stopTime.setText(formatTime(time));
//            TextView stopName = (TextView) v.findViewById(R.id.label_first_stop);
//            stopName.setText(name);
//            insertPoint.addView(v);

            for(int j = 0 ; j < busStops.size(); j++) {
                busStop = busStops.get(j);
                View busStopView = vi.inflate(R.layout.bus_stop, null);
                TextView textBusStop = (TextView) busStopView.findViewById(R.id.bus_stop);
                ImageView busStopImage = (ImageView) busStopView.findViewById(R.id.bus_stop_image);
                textBusStop.setText(busStop);
                TextView exitTime = (TextView) busStopView.findViewById(R.id.exit_time);


                if (j == 0) {
                    textBusStop.setTextColor(Color.BLACK);
                    exitTime.setText(formatTime((Date) time));
                    textBusStop.setTextSize(TypedValue.COMPLEX_UNIT_SP, 18);
                    textBusStop.setTypeface(null, Typeface.BOLD);
                    busStopImage.setVisibility(View.VISIBLE);
                    busStopImage.setImageResource(R.drawable.ic_directions_bus_black_24dp);
                    busStopView.setPadding(16, 8, 16, 4);
                }
                else if (j == busStops.size() - 1) {
                    textBusStop.setTextColor(Color.BLACK);
                    exitTime.setText(formatTime((Date) exit));
                    textBusStop.setTextSize(TypedValue.COMPLEX_UNIT_SP, 18);
                    textBusStop.setTypeface(null, Typeface.BOLD);
                    busStopImage.setVisibility(View.VISIBLE);
                    busStopImage.setImageResource(R.drawable.ic_directions_bus_black_24dp);
                    busStopView.setPadding(16,8,16,4);

                }
                else {
                    textBusStop.setTextColor(Color.BLACK);
                    exitTime.setVisibility(View.INVISIBLE);
                }
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

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void expandBusStopList(View view){
        if(!flagListVisible){
            recycler.setVisibility(View.VISIBLE);
            flagListVisible = true;
        }
        else {
            recycler.setVisibility(View.GONE);
            flagListVisible = false;
        }
    }

    private String formatTime(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        return timeFormat.format(calendar.getTime());
    }

}
