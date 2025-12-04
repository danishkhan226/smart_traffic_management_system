/* ============================================
   Enhanced AnimatedCounter Component
   ============================================ */

import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

export default function AnimatedCounter({
    value,
    duration = 1000,
    decimals = 0,
    prefix = '',
    suffix = '',
    className = ''
}) {
    const [count, setCount] = useState(0);
    const previousValueRef = useRef(value);

    useEffect(() => {
        const startValue = previousValueRef.current || 0;
        const endValue = value || 0;
        const diff = endValue - startValue;

        if (diff === 0) return;

        const startTime = Date.now();
        const timer = setInterval(() => {
            const now = Date.now();
            const progress = Math.min((now - startTime) / duration, 1);

            // Easing function (easeOutCubic)
            const easeProgress = 1 - Math.pow(1 - progress, 3);

            const currentCount = startValue + (diff * easeProgress);
            setCount(currentCount);

            if (progress === 1) {
                clearInterval(timer);
                setCount(endValue);
                previousValueRef.current = endValue;
            }
        }, 16); // ~60fps

        return () => clearInterval(timer);
    }, [value, duration]);

    const displayValue = decimals > 0
        ? count.toFixed(decimals)
        : Math.round(count);

    return (
        <span className={className}>
            {prefix}{displayValue}{suffix}
        </span>
    );
}

AnimatedCounter.propTypes = {
    value: PropTypes.number.isRequired,
    duration: PropTypes.number,
    decimals: PropTypes.number,
    prefix: PropTypes.string,
    suffix: PropTypes.string,
    className: PropTypes.string,
};
