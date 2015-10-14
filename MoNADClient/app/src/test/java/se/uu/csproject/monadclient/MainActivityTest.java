package se.uu.csproject.monadclient;

//import se.uu.csproject.BuildConfig;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.Robolectric;
import org.robolectric.RobolectricGradleTestRunner;
import org.robolectric.annotation.Config;

import static org.assertj.core.api.Assertions.*;

@RunWith(RobolectricGradleTestRunner.class)
@Config(constants = BuildConfig.class)
public class MainActivityTest {

  @Test
  public void testSomething() throws Exception {
    assertThat("test".isEqualTo("test");
  }
}
