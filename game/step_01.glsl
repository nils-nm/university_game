#define N 500

//x, y position of the light
uniform vec2 lightPosition;
//size of light in pixels
uniform float lightSize;

float terrain(vec2 samplePoint)
{
	float samplePointAlpha = texture(iChannel0, samplePoint).a;
	float sampleStepped = step(0.1, samplePointAlpha);
	float returnValue = 1.0 - sampleStepped;

	//soften the shadow !аномалия! 0.95 стены прозрачные, 0.97 стены черные.
	// при силе света 500. значение 0.96 подобрано методом научного тыка
	returnValue = mix(0.96, 1.0, returnValue);

	return returnValue;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	//distance in pixels to the light
	float distanceToLight = length(lightPosition - fragCoord);

	//normalize the fragment coordinate from (0,0) to (1,1)
	vec2 normalizedFragCoord = fragCoord/iResolution.xy;
	vec2 normalizedLightCoord = lightPosition.xy/iResolution.xy;

	//start our mixing variable at 1.0
	float lightAmount = 1.0;
	for(float i = 0.0; i < N; i++)
	{
		float t = i/N;
		//grab a coordinate between where we are and the light
		vec2 samplePoint = mix(normalizedFragCoord, normalizedLightCoord, t);

		float shadowAmount = terrain(samplePoint);
		//multiply the light amount
		lightAmount *= shadowAmount;
	}

	//find out how much light we have based on the distanse to our light
	lightAmount *= 1.0 - smoothstep(0.0, lightSize, distanceToLight);

	//we'll alternate our display between black and whatever is in channel 1
	vec4 blackColor = vec4(0.0, 0.0, 0.0, 1.0);

	//our fragment color will be somewhere between black and channel1
	fragColor = mix(blackColor, texture(iChannel1, normalizedFragCoord), lightAmount);
}
