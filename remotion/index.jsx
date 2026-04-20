import React from 'react';
import {Composition, registerRoot, staticFile} from 'remotion';
import {HomeHeroRemotion} from './HomeHeroRemotion';

const RemotionRoot = () => {
  return (
    <Composition
      id="HomeHeroRemodel"
      component={HomeHeroRemotion}
      durationInFrames={150}
      fps={30}
      width={1280}
      height={880}
      defaultProps={{
        oldHouseSrc: staticFile('images/hero-house-before.jpg'),
        newHouseSrc: staticFile('images/hero-house-after.jpg'),
      }}
    />
  );
};

registerRoot(RemotionRoot);
