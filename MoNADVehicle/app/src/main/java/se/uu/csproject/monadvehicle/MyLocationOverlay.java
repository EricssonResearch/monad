package se.uu.csproject.monadvehicle;

import org.mapsforge.core.graphics.Bitmap;
import org.mapsforge.core.graphics.Canvas;
import org.mapsforge.core.graphics.GraphicFactory;
import org.mapsforge.core.graphics.Paint;
import org.mapsforge.core.graphics.Style;
import org.mapsforge.core.model.BoundingBox;
import org.mapsforge.core.model.LatLong;
import org.mapsforge.core.model.Point;
import org.mapsforge.map.android.graphics.AndroidGraphicFactory;
import org.mapsforge.map.layer.Layer;
import org.mapsforge.map.layer.overlay.Circle;
import org.mapsforge.map.layer.overlay.Marker;
import org.mapsforge.map.model.MapViewPosition;

import android.content.Context;
import android.location.Location;
import android.location.LocationProvider;
import android.os.Handler;
import android.util.Log;

import com.google.android.gms.location.LocationListener;

import java.util.ArrayList;
import java.util.ListIterator;

/**
 * A thread-safe {@link Layer} implementation to display the current location. Use the new location services provided by Google
 * Play Services. Note that MyLocationOverlay needs to be added to a view before requesting location updates
 * (otherwise no DisplayModel is set).
 */
public class MyLocationOverlay extends Layer implements LocationListener {
	private static final GraphicFactory GRAPHIC_FACTORY = AndroidGraphicFactory.INSTANCE;
	private final int RADIUS = 40;

	private ArrayList<LatLong> trajectory;

    /**
     * The listener interface is used in MainActivity
     * It updates the bus stop data based on the LocationChanged function
     */
    public interface Listener {
        void onLocationChange(Location location);
    }

    private Listener mListener = null;
    public void registerListener (Listener listener) {
        mListener = listener;
    }

    LatLong tmp;
    ListIterator<LatLong> ite;

	/**
	 * @param location
	 *            the location whose geographical coordinates should be converted.
	 * @return a new LatLong with the geographical coordinates taken from the given location.
	 */
	public static LatLong locationToLatLong(Location location) {
		return new LatLong(location.getLatitude(), location.getLongitude(), true);
	}

	private static Paint getDefaultCircleFill() {
		return getPaint(GRAPHIC_FACTORY.createColor(48, 0, 0, 255), 0, Style.FILL);
	}

	private static Paint getDefaultCircleStroke() {
		return getPaint(GRAPHIC_FACTORY.createColor(160, 0, 0, 255), 2, Style.STROKE);
	}

	private static Paint getPaint(int color, int strokeWidth, Style style) {
		Paint paint = GRAPHIC_FACTORY.createPaint();
		paint.setColor(color);
		paint.setStrokeWidth(strokeWidth);
		paint.setStyle(style);
		return paint;
	}

	private boolean centerAtNextFix;
	private final Circle circle;
	private final MapViewPosition mapViewPosition;
	private final Marker marker;
	private boolean snapToLocationEnabled;

	/**
	 * Constructs a new {@code MyLocationOverlay} with the default circle paints.
	 *
	 * @param context
	 *            a reference to the application context.
	 * @param mapViewPosition
	 *            the {@code MapViewPosition} whose location will be updated.
	 * @param bitmap
	 *            a bitmap to display at the current location (might be null).
	 */
	public MyLocationOverlay(Context context, MapViewPosition mapViewPosition, Bitmap bitmap) {
		this(context, mapViewPosition, bitmap, getDefaultCircleFill(), getDefaultCircleStroke());
	}

	/**
	 * Constructs a new {@code MyLocationOverlay} with the given circle paints.
	 *
	 * @param context
	 *            a reference to the application context.
	 * @param mapViewPosition
	 *            the {@code MapViewPosition} whose location will be updated.
	 * @param bitmap
	 *            a bitmap to display at the current location (might be null).
	 * @param circleFill
	 *            the {@code Paint} used to fill the circle that represents the accuracy of the current location (might be null).
	 * @param circleStroke
	 *            the {@code Paint} used to stroke the circle that represents the accuracy of the current location (might be null).
	 */
	public MyLocationOverlay(Context context, MapViewPosition mapViewPosition, Bitmap bitmap, Paint circleFill,
							 Paint circleStroke) {
		super();

		this.mapViewPosition = mapViewPosition;
		this.marker = new Marker(null, bitmap, 0, 0);
		this.circle = new Circle(null, 0, circleFill, circleStroke);
	}

    public ArrayList<LatLong> getTrajectory() {
        return trajectory;
    }

    public void setTrajectory(ArrayList<LatLong> trajectory) {
        this.trajectory = trajectory;
        ite = trajectory.listIterator();
    }

	@Override
	public synchronized void draw(BoundingBox boundingBox, byte zoomLevel, Canvas canvas, Point topLeftPoint) {
		this.circle.draw(boundingBox, zoomLevel, canvas, topLeftPoint);
		this.marker.draw(boundingBox, zoomLevel, canvas, topLeftPoint);
	}

	/**
	 * Enables the receiving of location updates from the most accurate {@link LocationProvider} available.
	 *
	 * @param centerAtFirstFix
	 *            whether the map should be centered to the first received location fix.
	 * @return true if at least one location provider was found, false otherwise.
	 */
	public synchronized boolean enableMyLocation(boolean centerAtFirstFix) {
		this.centerAtNextFix = centerAtFirstFix;
		this.circle.setDisplayModel(this.displayModel);
		this.marker.setDisplayModel(this.displayModel);
		return true;
	}

	@Override
	public void onDestroy() {
		this.marker.onDestroy();
	}

	@Override
	public void onLocationChanged(Location location) {

		synchronized (this) {
			//remove it when necessary
			//Log.i("current location", location.getLatitude() + ", " + location.getLongitude());

            //TODO: Remove the if check and the currPos initialization when deploying the app
            if(ite.hasNext()) {
                tmp = ite.next();
                Location currPos = new Location("");
                currPos.setLatitude(tmp.latitude);
                currPos.setLongitude(tmp.longitude);
            //end of removal task

            //TODO: Replace "currPos" occurrences with "location"
                Storage.setCurrentLocation(currPos);
                if (mListener != null) {
                    mListener.onLocationChange(currPos);
                }

                LatLong latLong = locationToLatLong(currPos);

                this.marker.setLatLong(latLong);
                this.circle.setLatLong(latLong);
                if (location.getAccuracy() != 0) {
                    this.circle.setRadius(location.getAccuracy());
                } else {
                    // on the emulator we do not get an accuracy
                    this.circle.setRadius(RADIUS);
                }

                if (this.centerAtNextFix || this.snapToLocationEnabled) {
                    this.centerAtNextFix = false;
                    this.mapViewPosition.setCenter(latLong);
                }

                requestRedraw();
            }
		}
	}

	/**
	 * @param snapToLocationEnabled
	 *            whether the map should be centered at each received location fix.
	 */
	public synchronized void setSnapToLocationEnabled(boolean snapToLocationEnabled) {
		this.snapToLocationEnabled = snapToLocationEnabled;
	}

	/* testing with fake coordinates
	public void moveSimulate(){
		SimulateThread simulateThread = new SimulateThread();
		simulateThread.start();
	}

	class SimulateThread extends Thread {
        public void run() {

			while(ite.hasNext()){
                tmp = ite.next();
                Log.w("move", tmp.latitude + ", " + tmp.longitude);

                Location currPos = new Location("");
                currPos.setLatitude(tmp.latitude);
                currPos.setLongitude(tmp.longitude);
                Storage.setCurrentLocation(currPos);
                if (mListener != null) {
                    mListener.onLocationChange(currPos);
                }
				try {
					sleep(500);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
	}*/
}