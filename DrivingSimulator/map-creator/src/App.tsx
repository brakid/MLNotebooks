import React, { useEffect, useRef } from 'react';

const App = () => {
  const canvasReference = useRef<HTMLCanvasElement>(null);
  const isDrawing = useRef<boolean>(false);  

  useEffect(() => {
    console.log(canvasReference.current);

    if (canvasReference.current) {
      const drawContext = canvasReference.current.getContext('2d');
      if (drawContext) {
        drawContext.fillStyle = '#000000';
      }

      const startDrawing = (event: MouseEvent): void => {
        event.preventDefault();
        console.log(event);
        //setIsDrawing(() => true);
        isDrawing.current = true;
      };
    
      const stopDrawing = (event: MouseEvent): void => {
        event.preventDefault();
        console.log(event);
        //setIsDrawing(() => false);
        isDrawing.current = false;
      };
    
      const drawing = (event: MouseEvent): void => {
        event.preventDefault();
    
        const x = event.pageX - 11
        const y = event.pageY - 11;

        if (isDrawing.current === true) {
          console.log(x, y);
          if (drawContext) {
            drawContext.fillRect(x-10, y-10, 20, 20);
          }
        }
      };

      canvasReference.current.addEventListener('mousedown', startDrawing);
      canvasReference.current.addEventListener('mouseup', stopDrawing);
      canvasReference.current.addEventListener('mouseleave', stopDrawing);
      canvasReference.current.addEventListener('mousemove', drawing);
    }
  }, [canvasReference]);

  return (
    <canvas
        width={ 400 }
        height={ 400 }
        style={{ border: '1px solid black', position: 'absolute', top: '10px', left: '10px' }} 
        ref={ canvasReference } />
  );
};

export default App;
