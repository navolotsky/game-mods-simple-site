import s from './DefaultButton.module.css';

const DefaultButton = ({children, ...props}) => {
    return (
        <div {...props} className={s.DefaultButton}>
            {children}
        </div>
    );
};

export default DefaultButton;
