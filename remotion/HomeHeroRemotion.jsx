import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const PIECES_X = 5;
const PIECES_Y = 4;
const TOTAL_PIECES = PIECES_X * PIECES_Y;

const pieceStyle = ({col, row, pieceWidth, pieceHeight, progress, direction, imageSrc, isEntering}) => {
  const index = row * PIECES_X + col;
  const xSeed = (col - (PIECES_X - 1) / 2) * 110;
  const ySeed = (row - (PIECES_Y - 1) / 2) * 95;
  const rotateBase = (index % 2 === 0 ? 1 : -1) * (10 + (index % 4) * 4);
  const distance = isEntering ? 1 - progress : progress;
  const translateX = xSeed * direction * distance;
  const translateY = ySeed * distance - 40 * distance;
  const rotate = rotateBase * distance;
  const scale = isEntering ? interpolate(progress, [0, 1], [0.86, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : interpolate(progress, [0, 1], [1, 0.88], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const opacity = isEntering ? progress : 1 - progress * 0.98;

  return {
    position: 'absolute',
    left: `${(col / PIECES_X) * 100}%`,
    top: `${(row / PIECES_Y) * 100}%`,
    width: `${pieceWidth}%`,
    height: `${pieceHeight}%`,
    overflow: 'hidden',
    borderRadius: 18,
    opacity,
    transform: `translate3d(${translateX}px, ${translateY}px, 0) rotate(${rotate}deg) scale(${scale})`,
    boxShadow: '0 14px 30px rgba(31, 41, 51, 0.18)',
    willChange: 'transform, opacity',
    backfaceVisibility: 'hidden',
    contain: 'paint',
    zIndex: isEntering ? 3 : 2,
  };
};

const PieceImage = ({src, col, row, progress, direction, isEntering}) => {
  const pieceWidth = 100 / PIECES_X;
  const pieceHeight = 100 / PIECES_Y;

  return (
    <div style={pieceStyle({col, row, pieceWidth, pieceHeight, progress, direction, imageSrc: src, isEntering})}>
      <Img
        src={src}
        style={{
          width: `${PIECES_X * 100}%`,
          height: `${PIECES_Y * 100}%`,
          maxWidth: 'none',
          maxHeight: 'none',
          marginLeft: `-${col * 100}%`,
          marginTop: `-${row * 100}%`,
          objectFit: 'cover',
        }}
      />
    </div>
  );
};

export const HomeHeroRemotion = ({oldHouseSrc, newHouseSrc}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const explodeStart = 36;
  const explodeDuration = 36;
  const rebuildStart = 80;
  const rebuildDuration = 34;

  const explodeProgress = interpolate(frame, [explodeStart, explodeStart + explodeDuration], [0, 1], {
    easing: Easing.bezier(0.22, 1, 0.36, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const rebuildProgress = interpolate(frame, [rebuildStart, rebuildStart + rebuildDuration], [0, 1], {
    easing: Easing.bezier(0.2, 0.9, 0.2, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const settle = spring({
    fps,
    frame: Math.max(0, frame - rebuildStart),
    config: {damping: 14, stiffness: 120, mass: 0.9},
  });

  const oldOpacity = interpolate(frame, [0, explodeStart + explodeDuration - 8], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const newOpacity = interpolate(frame, [rebuildStart - 8, rebuildStart + rebuildDuration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const flashOpacity = interpolate(frame, [60, 76, 92], [0, 0.92, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const oldScale = interpolate(frame, [0, explodeStart], [1.01, 1.04], {
    extrapolateRight: 'clamp',
  });
  const newScale = interpolate(settle, [0, 1], [1.08, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#f5efe5', fontFamily: 'Inter, system-ui, sans-serif'}}>
      <AbsoluteFill
        style={{
          background: 'radial-gradient(circle at top, rgba(255,255,255,0.85), rgba(255,255,255,0) 45%), linear-gradient(180deg, #f8f2e8 0%, #eadfce 100%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: '6% 6% 8%',
          borderRadius: 36,
          overflow: 'hidden',
          boxShadow: '0 30px 60px rgba(31, 41, 51, 0.18)',
          background: '#e7ded0',
        }}
      >
        <AbsoluteFill style={{opacity: oldOpacity}}>
          <Img src={oldHouseSrc} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${oldScale})`}} />
        </AbsoluteFill>

        {Array.from({length: TOTAL_PIECES}).map((_, index) => {
          const col = index % PIECES_X;
          const row = Math.floor(index / PIECES_X);
          return <PieceImage key={`old-${index}`} src={oldHouseSrc} col={col} row={row} progress={explodeProgress} direction={index % 2 === 0 ? -1 : 1} isEntering={false} />;
        })}

        <AbsoluteFill style={{opacity: newOpacity, transform: `scale(${newScale})`}}>
          <Img src={newHouseSrc} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </AbsoluteFill>

        {Array.from({length: TOTAL_PIECES}).map((_, index) => {
          const col = index % PIECES_X;
          const row = Math.floor(index / PIECES_X);
          return <PieceImage key={`new-${index}`} src={newHouseSrc} col={col} row={row} progress={rebuildProgress} direction={index % 2 === 0 ? 1 : -1} isEntering />;
        })}

        <AbsoluteFill
          style={{
            opacity: flashOpacity,
            background: 'radial-gradient(circle, rgba(255,255,255,0.95) 0%, rgba(245,225,196,0.5) 42%, rgba(245,225,196,0) 72%)',
            mixBlendMode: 'screen',
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: 32,
            right: 32,
            bottom: 28,
            height: 120,
            borderRadius: 999,
            background: 'linear-gradient(180deg, rgba(59,130,88,0), rgba(59,130,88,0.25))',
            filter: 'blur(12px)',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
