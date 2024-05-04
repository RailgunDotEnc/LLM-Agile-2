'use client';
import {styled} from "@mui/material/styles";
import Button from "@mui/material/Button";
import InputBase from '@mui/material/InputBase';
import {alpha} from "@mui/material";
import Switch from '@mui/material/Switch';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';


export const CustomTabs = styled((props) => (
    <Tabs
        {...props}
        TabIndicatorProps={{ children: <span className="MuiTabs-indicatorSpan" /> }}
    />
))({
    '& .MuiTabs-indicator': {
        display: 'flex',
        justifyContent: 'center',
        backgroundColor: 'transparent',
    },
    '& .MuiTabs-indicatorSpan': {
        maxWidth: 40,
        width: '100%',
        backgroundColor: '#635ee7',
    },
});

export const CustomTab = styled((props) => <Tab disableRipple {...props} />)(({ theme }) => ({
    textTransform: 'none',
    minWidth: 0,
    [theme.breakpoints.up('sm')]: {
        minWidth: 0,
    },
    fontWeight: theme.typography.fontWeightRegular,
    marginRight: theme.spacing(1),
    color: 'rgba(0, 0, 0, 0.85)',
    fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
    ].join(','),
    '&:hover': {
        color: '#40a9ff',
        opacity: 1,
    },
    '&.Mui-selected': {
        color: '#1890ff',
        fontWeight: theme.typography.fontWeightMedium,
    },
    '&.Mui-focusVisible': {
        backgroundColor: '#d1eaff',
    },
}));


export const CustomButton = styled(Button)({
    boxShadow: 'none',
    textTransform: 'none',
    fontSize: 16,
    padding: '6px 12px',
    border: '1px solid',
    lineHeight: 1.5,
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    color: '#14213D',
    fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
    ].join(','),
    '&:hover': {
        backgroundColor: 'transparent',
        borderColor: 'transparent',
        boxShadow: 'none',
        textDecoration: 'underline',
        textDecorationColor: '#14213D'
    },
    '&:active': {
        boxShadow: 'none',
    },
});

export const PrimaryButtonWithBackground = styled(CustomButton)({
    backgroundColor: '#ffffff',
    border: '1.5px solid #14213D',
    borderRadius: '.5rem',
    color: '#14213D',
    '&:hover': {
        backgroundColor: '#d7e4f1',
        color: '#14213D',
        textDecorationColor: 'transparent'
    },
});
export const DestructiveButtonWithBackground = styled(CustomButton)({
    backgroundColor: '#d30303',
    borderRadius: '.5rem',
    color: '#ffffff',
    '&:hover': {
        backgroundColor: '#ffc3c3',
        color: '#d30303',
        textDecorationColor: 'transparent'
    },
});

// Variation with purple outline
export const CustomButtonWithOutline = styled(CustomButton)({
    borderColor: '#14213D',
    '&:active': {
        backgroundColor: '#FCA311',
        color: '#14213D',
        textDecorationColor: 'transparent'
    },
    '&:hover': {
        backgroundColor: '#FCA311',
        color: '#14213D',
        textDecorationColor: 'transparent'
    },
});

// Variation with background
export const CustomButtonWithBackground = styled(CustomButton)({
    backgroundColor: '#14213D',
    borderRadius: '.5rem',
    color: '#E5E5E5',
    '&:hover': {
        backgroundColor: '#FCA311',
        color: '#14213D',
        textDecorationColor: 'transparent'
    },
});

export const CustomSecondaryButtonWithBackground = styled(CustomButton)({
    backgroundColor: '#ffffff',
    borderRadius: '.5rem',
    color: '#14213D',
    '&:hover': {
        backgroundColor: '#14213D',
        color: '#ffffff',
        textDecorationColor: 'transparent'
    },
});
export const CustomSwitch = styled(Switch)(({ theme }) => ({
    width: 28,
    height: 16,
    padding: 0,
    display: 'flex',
    '&:active': {
        '& .MuiSwitch-thumb': {
            width: 15,
        },
        '& .MuiSwitch-switchBase.Mui-checked': {
            transform: 'translateX(9px)',
        },
    },
    '& .MuiSwitch-switchBase': {
        padding: 2,
        '&.Mui-checked': {
            transform: 'translateX(12px)',
            color: '#fff',
            '& + .MuiSwitch-track': {
                opacity: 1,
                backgroundColor: theme.palette.mode === 'dark' ? '#177ddc' : '#1890ff',
            },
        },
    },
    '& .MuiSwitch-thumb': {
        boxShadow: '0 2px 4px 0 rgb(0 35 11 / 20%)',
        width: 12,
        height: 12,
        borderRadius: 6,
        transition: theme.transitions.create(['width'], {
            duration: 200,
        }),
    },
    '& .MuiSwitch-track': {
        borderRadius: 16 / 2,
        opacity: 1,
        backgroundColor:
            theme.palette.mode === 'dark' ? 'rgba(255,255,255,.35)' : 'rgba(0,0,0,.25)',
        boxSizing: 'border-box',
    },
}));

export const HeroButtonWithBackground = styled(CustomButton)({
    backgroundColor: '#FCA311',
    borderRadius: '.5rem',
    color: '#14213D',
    '&:hover': {
        backgroundColor: '#14213D',
        color: '#E5E5E5',
        textDecorationColor: 'transparent'
    },
});

export const AppInputBox = styled(InputBase)(({ theme }) => ({
    'label + &': {
        marginTop: theme.spacing(3),
    },
    '& .MuiInputBase-input': {
        borderRadius: '1rem',
        position: 'relative',
        backgroundColor: '#F5F5F5',
        //border: '1px solid',
        //borderColor: theme.palette.mode === 'light' ? '#E0E3E7' : '#2D3843',
        fontSize: 16,
        //width: 'auto',
        padding: '10px 12px',
        transition: theme.transitions.create([
            'border-color',
            'background-color',
            'box-shadow',
        ]),
        // Use the system font instead of the default Roboto font.
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(','),
        '&:focus': {
            boxShadow: `${alpha('#FCA311', 0.25)} 0 0 0 0.2rem`,
            borderColor: '1px solid #FCA311',
        },
    },
}));
